from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    preferences = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', preferences='{self.preferences}')>"

# Connecting to a SQLite database
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)

# Create a session to work with the data
Session = sessionmaker(bind=engine)
session = Session()

# List of possible categories
categories = ['technology', 'science', 'health', 'Sports', 'business', 'general']


def add_user(username, email, chosen_categories):
    """
The function adds a new user to the database.
The function checks if his email already exists in the database
i.e. if the user already exists, in which case it will not add him again
if not, it creates a new user with a name, email, and preferred categories and adds him 
to the database
    """
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
  
  """
The function is designed to update user preferences
The function receives an email and new preferences
Checks if the user exists based on the email and if so performs the update
    """
  # Finding the user by email
  user_to_update = session.query(User).filter_by(email=email).first()
    
  if user_to_update:
        user_to_update.preferences = ','.join(new_preferences) 
        session.commit()
        session.refresh(user_to_update)  
        print(f"User updated: {user_to_update}")  
        return user_to_update
  else:
      print("User not found")

#update_user_preferences('deniss4293@gmail.com','Technology, Travel')


users = session.query(User).all()
#print(type(users))  
print(users)       

#for user in users:
    #print(user)

#user_to_delete = session.query(User).filter_by(email='   ').first()  
#session.delete(user_to_delete)
#session.commit()

session.close()  