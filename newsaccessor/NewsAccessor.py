import httpx
import os
from dotenv import load_dotenv

load_dotenv()  

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

#The function makes an asynchronous call to the newsapi.org API to pull up-to-date news.
async def fetch_news_data():
    if not NEWS_API_KEY:
        raise ValueError("API Key is missing!")  
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # If the API request is unsuccessful,it will automatically throw an error.
        data = response.json()
        return data
