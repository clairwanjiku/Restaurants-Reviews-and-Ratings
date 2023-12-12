from models import Base, Restaurant, Customer, Review
from database import Session

# Create a session
session = Session()

# Add data
restaurant1 = Restaurant(name='sarova hotel', price=2000)
restaurant2 = Restaurant(name='Mishis hotel', price=5722)
restaurant3 = Restaurant(name='mara hotel', price=430)

customer1 = Customer(first_name='Clair', last_name='Karanja')
customer2 = Customer(first_name='Basil', last_name='Kamande')
customer3 = Customer(first_name='Anyango', last_name='Okeochi')

review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
review2 = Review(star_rating=5, restaurant=restaurant2, customer=customer2)
review3 = Review(star_rating=5, restaurant=restaurant3, customer=customer3)

session.add_all([restaurant1, restaurant2, restaurant3, customer1, customer2, customer3, review1, review2, review3])
session.commit()

# Perform queries
customer1_reviews = session.query(Customer).filter_by(first_name='Clair').first().reviews
for review in customer1_reviews:
    print(f"Review for {review.restaurant.name} ({review.restaurant.id}), Price: {review.restaurant.price}, by {review.customer.full_name()} ({review.customer.id}): {review.star_rating} stars")

customer2_reviews = session.query(Customer).filter_by(first_name='Basil').first().reviews
for review in customer2_reviews:
    print(f"Review for {review.restaurant.name} ({review.restaurant.id}), Price: {review.restaurant.price}, by {review.customer.full_name()} ({review.customer.id}): {review.star_rating} stars")

# Close the session
session.close()
