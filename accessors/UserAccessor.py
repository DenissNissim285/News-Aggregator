from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# הגדרת בסיס ה-ORM
Base = declarative_base()

# הגדרת טבלת משתמשים
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    preferences = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', preferences='{self.preferences}')>"

# חיבור למסד נתונים SQLite
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)

# יצירת סשן לעבודה עם הנתונים
Session = sessionmaker(bind=engine)
session = Session()

# רשימת הקטגוריות האפשריות
categories = ['technology', 'sports', 'health', 'politics', 'business', 'travel']


# הוספת משתמש חדש
# בדיקה אם האימייל כבר קיים במסד הנתונים
def add_user(username, email, chosen_categories):
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        print(f"The email {email} already exists in the DB")
        return None
    
    preferences = ','.join(chosen_categories)
    new_user = User(username=username, email=email, preferences=preferences)
    session.add(new_user)
    session.commit()
    print(f"User {username} added successfully")
    return new_user



    #new_user = User(username='Deniss', email='deniss4293@gmail.com', preferences='Technology, Travel')
    #session.add(new_user)
    #session.commit()


def update_preferences(email, new_preferences):
    # מציאת המשתמש לפי אימייל
    user_to_update = session.query(User).filter_by(email=email).first()
    
    if user_to_update:
        # עדכון העדפות המשתמש לפי הרשימה החדשה
        user_to_update.preferences = ','.join(new_preferences)  # שמירת ההעדפות בפורמט מופרד בפסיקים
        session.commit()
        print("User preferences have been updated")
        return user_to_update
    else:
        print("User not found")

#update_user_preferences('deniss4293@gmail.com','Technology, Travel')


# שליפת משתמשים מהמסד
users = session.query(User).all()
print(type(users))  # בדיקת סוג האובייקט
print(users)        # הדפסת הנתונים

#for user in users:
    #print(user)

session.close()  # סגירת הסשן לאחר סיום פעולת קריאה/כתיבה
