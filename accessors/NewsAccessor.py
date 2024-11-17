import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # טוען את משתני הסביבה מקובץ .env

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def fetch_news_data():
    if not NEWS_API_KEY:
        raise ValueError("API Key is missing!")  # אם לא נמצא מפתח
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # יזרוק שגיאה אם יש בעיה בבקשה
        data = response.json()
        return data
