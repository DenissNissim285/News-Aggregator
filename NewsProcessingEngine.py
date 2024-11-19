from accessors.HFAccessor import fetch_sorted_news_from_hugging_face

async def news_sorting(news, users, hugging_face_api_key):
    """
The function receives the news, users, and the API
The function sorts the news according to user preferences, using the Hugging Face accessor
    """
    user_news = {}  

    for user in users:
        user_id = user.id
        username = user.username
        email = user.email
        preferences = user.preferences.split(",")  
        matched_news = []  

        for article in news.get("articles", []):
            title = article.get("title", "")
            description = article.get("description", "")
            content = article.get("content", "")
            text = f"{title} {description} {content}"  

            # Call for HF accessor
            try:
                prediction = await fetch_sorted_news_from_hugging_face(text, preferences, hugging_face_api_key)
                
                # Add a check to indicate a match
                if prediction and prediction.get("labels"):
                    best_match = prediction["labels"][0] 
                    best_score = prediction["scores"][0]  
                    if best_match in preferences and best_score > 0.7:  
                        matched_news.append(article)
            except Exception as e:
                print(f"Error occurred while fetching data from Hugging Face: {e}")

        user_news[email] = {
            "id": user_id,
            "username": username,
            "email": email,
            "preferences": preferences,
            "news": matched_news,
        }

    return user_news


