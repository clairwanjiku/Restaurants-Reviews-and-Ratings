from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, comment='Unique ID for restaurant')
    name = Column(String, comment='Name of the restaurant')
    price = Column(Integer, comment='Price range of the restaurant')
    reviews = relationship("Review", back_populates="restaurant")

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, comment='Unique ID for customer')
    first_name = Column(String, comment='First name of the customer')
    last_name = Column(String, comment='Last name of the customer')
    reviews = relationship("Review", back_populates="customer")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def restaurants(self):
        return [review.restaurant for review in self.reviews]

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, comment='Unique ID for review')
    star_rating = Column(Integer, comment='Rating for the review')
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), comment='ID of the associated restaurant')
    customer_id = Column(Integer, ForeignKey('customers.id'), comment='ID of the associated customer')
    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars"
