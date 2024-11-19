from typing import List
from fastapi import BackgroundTasks, FastAPI, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
#from NewsProcessingEngine import DataManager
from dotenv import load_dotenv
import os
from accessors.UserAccessor import  User, add_user, update_preferences
from accessors.NewsAccessor import fetch_news_data
from accessors.EmailAccessor import send_news_to_users
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from NewsProcessingEngine import news_sorting 
from pydantic import BaseModel


#load_dotenv()  # טוען את המשתנים מקובץ .env

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print("Loaded API Key:", NEWS_API_KEY)  # בדיקה שהמפתח נטען

app = FastAPI()
print("Starting the server...")
templates = Jinja2Templates(directory="C:/Users/User/Desktop/Final_Project/templates")

#data_manager = DataManager()
import logging

# הגדרת לוגינג
logging.basicConfig(level=logging.DEBUG)  # הצגת לוגים ברמת DEBUG ומעלה

logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fetch-news", response_class=JSONResponse)
async def fetch_news():
    #news=await fetch_news_data()
    return await fetch_news_data()
    

# חיבור למסד נתונים SQLite
engine = create_engine('sqlite:///users.db')

# יצירת סשן (session)
Session = sessionmaker(bind=engine)
session = Session()  # יצירת ה-session

# הוספת משתמש חדש
new_user = add_user('Deniss', 'deniss4293@gmail.com', ['business', 'sports', 'general'])
if new_user:
    print(f"New user added: {new_user}")

# עדכון העדפות של משתמש
updated_user = update_preferences('deniss4293@gmail.com', ['business', 'health'])
if updated_user:
    print(f"User preferences updated: {updated_user}")



@app.get("/get-matched-news", response_class=JSONResponse)
async def get_matched_news(request: Request, categories: list[str] = Query([])):
    try:
        print(f"Categories received: {categories}")  # הדפסת הקטגוריות שנשלחו

        if not categories:
            return JSONResponse(status_code=400, content={"message": "No categories selected"})

        # שליפת החדשות מה-API
        news = await fetch_news_data()  # מחכה לתוצאה של fetch_news_data
        print("Fetched news:", news)

        # אם אין חדשות, שלח תשובה מתאימה
        if not news:
            return JSONResponse(status_code=404, content={"message": "No news found"})

        # סינון החדשות לפי הקטגוריות שנבחרו
        # קבלת כל המשתמשים
        users = session.query(User).all()
        print("Fetched users:", users)
        
        # המרת העדפות למבנה רשימה
        user_news = await news_sorting(news, users)  # קריאה למנוע
        
        print("Filtered news:", user_news)

        if not user_news:
            return JSONResponse(status_code=404, content={"message": "No news available for the selected categories"})

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
        # קריאה לאקססור לעדכון העדפות
        updated_user = update_preferences(request.email, request.preferences)

        if updated_user:
            # החזרת המידע של המשתמש המעודכן
            return JSONResponse(
                status_code=200, 
                content={"message": "Preferences updated successfully", "user": {"email": updated_user.email, "preferences": updated_user.preferences}}
            )
        else:
            # אם המשתמש לא נמצא, החזרת שגיאה
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Internal Server Error: {str(e)}"})
    # קריאה עם העדפות מעודכנות
    user_news = await news_sorting(news, users)  # קריאה למנוע
    


# מבנה הבקשה ליצירת משתמש חדש
class SetPreferencesRequest(BaseModel):
    username: str
    email: str
    preferences: list[str]

@app.post("/set-preferences")
async def set_preferences_endpoint(request: SetPreferencesRequest):
    try:
        # קריאה לפונקציה add_user מהאקססור
        new_user = add_user(
            username=request.username,
            email=request.email,
            chosen_categories=request.preferences
        )
        
        # בדיקה אם המשתמש נוסף
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
        # אימות נתונים
        if not request.email or not isinstance(request.news, list):
            return JSONResponse(status_code=400, content={"message": "Invalid request data"})

        # ווידוא שהחדשות הן מחרוזות בלבד
        if not all(isinstance(title, str) for title in request.news):
            return JSONResponse(status_code=400, content={"message": "Invalid news format. Titles must be strings."})

        # קריאה לאקססור
        background_tasks.add_task(send_news_to_users, [{"email": request.email, "news": request.news}], background_tasks)
        return {"status": "accepted", "message": "Emails are being processed and sent"}
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}
