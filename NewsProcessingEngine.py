# Categories and keywords for each
CATEGORY_KEYWORDS = {
    "technology": ["ai", "cloud", "blockchain", "robotics", "programming", "cybersecurity", "apple", "google", "microsoft", "android", "iphone", "software", "hardware", "innovation", "tech", "gadget", "machine learning", "data science", "virtual reality", "internet of things", "5G", "cyber attack", "automation", "startup", "tech news"],
    "science": ["science", "research", "study", "biology", "physics", "astronomy", "chemistry", "space", "experiment", "genetics", "medicine", "genomics","chemistry", "molecules", "atoms", "chemical reactions", "organic chemistry", "inorganic chemistry", "pharmaceuticals", "catalysts", "periodic table", "bonding", "elements", "compounds", "mixtures", "solutions", "acids", "bases", "pH", "stoichiometry", "chemical engineering", "polymer" "environment", "earth", "climate", "fossils", "evolution", "natural selection", "molecules", "atoms", "biotechnology", "lab", "scientific method", "earthquake", "oceanography"],
    "health": ["health", "hospital", "doctor", "fitness", "medicine", "virus", "disease", "healthcare", "wellness", "mental health", "exercise", "nutrition", "vaccine", "pandemic", "public health", "cardiology", "oncology", "surgery", "health tips", "diagnosis", "prevention", "hygiene", "treatment", "rehabilitation", "chronic illness", "pharmacy"],
    "sports": ["sport", "game", "football", "soccer", "basketball", "tennis", "olympics", "athletics", "rugby", "golf", "swimming", "MMA", "baseball", "hockey", "boxing", "championship", "team", "competition", "win", "match", "coach", "player", "goal", "fifa", "nba", "sports news", "olympic games", "track and field", "formula 1", "sports injuries"],
    "business": ["business", "industry", "company", "finance", "economy", "stocks", "investment", "startup", "market", "management", "entrepreneur", "profit", "corporate", "sales", "marketing", "strategy", "growth", "startup culture", "investment strategies", "business news", "merger", "acquisition", "business model", "economics", "leadership", "financial analysis", "small business", "brand", "advertising", "capital", "business development", "banking"],
    "general": ["news", "world", "events", "politics", "culture", "society", "international", "breaking", "current affairs", "worldwide", "headline", "update", "media", "history", "education", "government", "justice", "rights", "law", "human rights", "elections", "corruption", "news updates", "social media", "opinion", "public policy", "international relations", "global warming", "social issues"]
}

def extract_keywords(text):
    words = text.lower().split()
    return set(words)

async def news_sorting(news, users):
    """
    The function is responsible for sorting news articles according to user preferences.
    It receives a list of news and a list of users and returns an object containing the 
    sponsored news for each user according to their preferences.
    """
    user_news = {}

    for user in users:
        user_id = user.id
        username = user.username
        email = user.email
        preferences = user.preferences.split(",")
        matched_news = []

        for article in news.get("articles", []):
            # Check if each of the fields is not None before we work with them
            title = article.get("title", "").lower() if article.get("title") else ""
            description = article.get("description", "").lower() if article.get("description") else ""
            content = article.get("content", "").lower() if article.get("content") else ""

           # If no text is found, we will continue to the next article
            if not (title or description or content):
                continue

            text = f"{title} {description} {content}"

           # Extract keywords from the article
            keywords = extract_keywords(text)

            for pref in preferences:
                if pref.lower() in CATEGORY_KEYWORDS:
                    category_keywords = CATEGORY_KEYWORDS[pref.lower()]
                    for keyword in category_keywords:
                       # If the word is in the article content, add the article to the list
                        if keyword in text:
                            matched_news.append(article)
                            break  

        # Create a list of articles that are relevant to the user
        user_news[email] = {
            "id": user_id,
            "username": username,
            "email": email,
            "preferences": preferences,
            "news": matched_news,
        }

    return user_news
