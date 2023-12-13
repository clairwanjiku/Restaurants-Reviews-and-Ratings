from tabulate import tabulate
from models import Base, Restaurant, Customer, Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection setup
engine = create_engine('sqlite:///restaurant_reviews.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Clear tables before adding data
session.query(Restaurant).delete()
session.query(Customer).delete()
session.query(Review).delete()
session.commit()

# Add data
restaurant1 = Restaurant(name='sarova hotel', price=2000)
restaurant2 = Restaurant(name='Mishis hotel', price=5722)
restaurant3 = Restaurant(name='mara hotel', price=430)
session.add_all([restaurant1, restaurant2, restaurant3])

customer1 = Customer(first_name='Clair', last_name='Karanja')
customer2 = Customer(first_name='Basil', last_name='Kamande')
customer3 = Customer(first_name='Anyango', last_name='Okeochi')
session.add_all([customer1, customer2, customer3])

review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
review2 = Review(star_rating=5, restaurant=restaurant2, customer=customer2)
review3 = Review(star_rating=5, restaurant=restaurant3, customer=customer3)
session.add_all([review1, review2, review3])

session.commit()

# Print information from the tables with headers
print("\n--- Restaurants ---")
restaurants = session.query(Restaurant).all()
print(tabulate([[r.id, r.name, r.price] for r in restaurants], headers=["ID", "Name", "Price"]))

print("\n--- Customers ---")
customers = session.query(Customer).all()
print(tabulate([[c.id, c.first_name, c.last_name] for c in customers], headers=["ID", "First Name", "Last Name"]))

print("\n--- Reviews ---")
reviews = session.query(Review).all()
print(tabulate([[r.id, r.star_rating, r.restaurant.name, r.customer.first_name, r.customer.last_name] for r in reviews], headers=["ID", "Rating", "Restaurant Name", "First Name", "Last Name"]))

# Close the session
session.close()
