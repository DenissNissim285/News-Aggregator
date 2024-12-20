from typing import List
from fastapi import BackgroundTasks, FastAPI, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
#from NewsProcessingEngine import DataManager
from dotenv import load_dotenv
import os
import logging
#import dapr.clients
import httpx
import uvicorn
from useraccessor.UserAccessor import  User, add_user, update_preferences
from newsaccessor.NewsAccessor import fetch_news_data
from emailaccessor.EmailAccessor import send_news_to_users
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from engine.engine import news_sorting 
from pydantic import BaseModel
import pika
import time


def connect_to_rabbitmq():
    retries = 5
    while retries > 0:
        try:
            print("Attempting to connect to RabbitMQ...")
            
            connection_params = pika.ConnectionParameters(
                host="rabbitmq",
                port=5672,
                credentials=pika.PlainCredentials("guest", "guest"),
                heartbeat=600,  # Keep the connection alive with a heartbeat every 10 minutes
                blocked_connection_timeout=300  # אפשר זמן לחיבור חסום ל-5 דקות
            )
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()
            print("Connected to RabbitMQ!")

            queue_name = 'my-queue' 
            channel.queue_declare(queue=queue_name, durable=True)  
            print(f"Queue '{queue_name}' is ready.")

           # Sending a message to the queue
            message = "test"  
            channel.basic_publish(
                exchange='',  
                routing_key=queue_name,  
                body=message,  
                properties=pika.BasicProperties(
                    delivery_mode=2, # Makes the message durable, so it won't be lost if RabbitMQ crashes
                )
            )
            print(f"Message sent to queue '{queue_name}': {message}")
            
            return channel
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            retries -= 1
            time.sleep(5)
    print("Failed to connect to RabbitMQ after several attempts.")
    return None


NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print("Loaded API Key:", NEWS_API_KEY)  # Check that the key is loaded
MY_API_KEY= os.getenv("MY_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="/app/templates")

#print("Starting the server...")
#templates = Jinja2Templates(directory="C:/Users/User/Desktop/Final_Project/templates")
#data_manager = DataManager()

@app.on_event("startup")
async def startup_event():
    connect_to_rabbitmq()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
     print("Home")
     return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fetch-news", response_class=JSONResponse)
async def fetch_news():
    return await fetch_news_data()

# Connecting to a SQLite database
engine = create_engine('sqlite:///users.db')

Session = sessionmaker(bind=engine)
session = Session()  

# Adding a new user
new_user = add_user('Deniss', 'deniss4293@gmail.com', ['business', 'sports', 'general'])
if new_user:
    print(f"New user added: {new_user}")

# Update user preferences
updated_user = update_preferences('deniss4293@gmail.com', ['business', 'health'])
if updated_user:
    print(f"User preferences updated: {updated_user}")


@app.get("/get-matched-news", response_class=JSONResponse)
async def get_matched_news(request: Request, categories: list[str] = Query([])):
    try:
        print(f"Categories received: {categories}") 
        if not categories:
            return JSONResponse(status_code=400, content={"message": "No categories selected"})

        # Retrieving the news from the API
        news = await fetch_news_data()  
        print("Fetched news:", news)

        # If there is no news, send an appropriate reply
        if not news:
            return JSONResponse(status_code=404, content={"message": "No news found"})

        users = session.query(User).all()
        print("Fetched users:", users)

        user_news = await news_sorting(news, users, MY_API_KEY)  # Call to engine
        
        print("Filtered news:", user_news)

        if not user_news:
            return JSONResponse(status_code=404, content={"message": "No news available for the selected categories"})

        # After filtering the news, send a message to RabbitMQ via Dapr
        async with httpx.AsyncClient() as client:
         response = await client.post(
            "http://manager-dapr:3500/v1.0/publish/rabbitmq/my-queue",  # Dapr HTTP API to publish
            json={"news": user_news}
        )
        print(f"News sent to RabbitMQ with status code: {response.status_code}")

        # Return the filtered news as the response
        return JSONResponse(content=user_news)

    except Exception as e:
        print(f"Error occurred: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

    

class UpdatePreferencesRequest(BaseModel):
    email: str
    preferences: list[str]

@app.put("/update-preferences")
async def update_preferences_endpoint(request: UpdatePreferencesRequest):
    try:
       # Calling the accessor to update preferences
        updated_user = update_preferences(request.email, request.preferences)

        if updated_user:
            # Return the updated user information
            return JSONResponse(
                status_code=200, 
                content={"message": "Preferences updated successfully", "user": {"email": updated_user.email, "preferences": updated_user.preferences}}
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Internal Server Error: {str(e)}"})
    # Calling the engine with updated preferences
 #   user_news = await news_sorting(news, users, MY_API_KEY) 
    

# The structure of the request to create a new user
class SetPreferencesRequest(BaseModel):
    username: str
    email: str
    preferences: list[str]

@app.post("/set-preferences")
async def set_preferences_endpoint(request: SetPreferencesRequest):
    try:
       # Calling the add_user function from the accessor
        new_user = add_user(
            username=request.username,
            email=request.email,
            chosen_categories=request.preferences
        )
        
       # Check if the user has been added
        if new_user:
            return {
                "message": f"User {request.username} added successfully",
                "user": {
                    "username": new_user.username,
                    "email": new_user.email,
                    "preferences": new_user.preferences
                }
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Email already exists in the database"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
      
class NewsItem(BaseModel):
    title: str  # Ensure the title is a string


class NewsEmailRequest(BaseModel):
    email: str
    news: List[str]

@app.post("/send-email")
async def send_news_email(request: NewsEmailRequest, background_tasks: BackgroundTasks):
    try:
        # Data validation
        if not request.email or not isinstance(request.news, list):
            return JSONResponse(status_code=400, content={"message": "Invalid request data"})

        # Making sure the news is just strings
        for title in request.news:
          if not isinstance(title, str):
            return JSONResponse(status_code=400, content={"message": "Invalid news format. Titles must be strings."})

       # Calling the accessor
        background_tasks.add_task(send_news_to_users, [{"email": request.email, "news": request.news}], background_tasks)
        return {"status": "accepted", "message": "Emails are being processed and sent"}
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)