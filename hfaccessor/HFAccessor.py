import asyncio
import httpx

async def fetch_sorted_news_from_hugging_face(article_text, preferences, hugging_face_api_key):
    """
The function accepts articles, preferences, and an API
Sending an article to the Hugging Face API for sorting by user preferences
returns a result that shows how relevant each category is to the text
    """
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"  # Address of the api that connects to the model
    headers = { # API verification
        "Authorization": f"Bearer {hugging_face_api_key}"
    }
    payload = { # Here we send the information that needs to be processed
        "inputs": article_text,  
        "parameters": {"candidate_labels": preferences}  
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()  # If the request fails, an error will be thrown
        return response.json() 
        
