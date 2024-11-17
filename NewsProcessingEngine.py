
import spacy

# טוען את המודל של spaCy (אפשר להוריד את המודל עם pip install spacy)
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    
    # חילוץ ישויות (entities) שמייצגות אנשים, ארגונים, תאריכים וכו'
    keywords = [ent.text.lower() for ent in doc.ents]
    
    # חילוץ מילות עצם ותארים
    keywords.extend([token.text.lower() for token in doc if token.pos_ in ['NOUN', 'ADJ']])
    
    return keywords

async def news_sorting(news, users):
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
            text = f"{title} {description}"
            keywords = extract_keywords(text)

            print(f"Keywords for article '{title}': {keywords}")

            for pref in preferences:
                if any(pref.lower() in keyword or keyword in pref.lower() for keyword in keywords):
                    if article not in matched_news:
                        print(f"Matched article: {title}")
                        matched_news.append(article)

        print(f"Matched news for {email}: {matched_news}")
        user_news[email] = {
            "id": user_id,
            "username": username,
            "email": email,
            "preferences": preferences,
            "news": matched_news,
        }

    print("User news:", user_news)
    return user_news
