
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
#from NewsProcessingEngine import DataManager
from dotenv import load_dotenv
import os
from accessors.UserAccessor import  User, add_user, update_preferences
from accessors.NewsAccessor import fetch_news_data
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from NewsProcessingEngine import news_sorting 

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
new_user = add_user('Deniss', 'deniss4293@gmail.com', ['business', 'sports', 'travel'])
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


      
     


