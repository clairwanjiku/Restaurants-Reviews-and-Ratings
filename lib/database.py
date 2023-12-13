from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Database connection setup
engine = create_engine('sqlite:///restaurant_reviews_and_ratings.db')
Session = sessionmaker(bind=engine)

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session
session = Session()

# Execute a query using SQLAlchemy (example)
results = session.execute('SELECT * FROM your_table_name').fetchall()
print(results)  # This will print the fetched data

# Close the session
session.close()
