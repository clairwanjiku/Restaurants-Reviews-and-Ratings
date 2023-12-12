from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database connection setup
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)

# Create tables in the database
Base.metadata.create_all(engine)
