from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///restaurant.sqlite', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    reviews = relationship('Review', back_populates='customer')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        if not self.reviews:
            return None
        return max(self.reviews, key=lambda review: review.star_rating).restaurant

    def add_review(self, restaurant, rating):
        new_review = Review(content='', star_rating=rating, customer=self, restaurant=restaurant)
        self.reviews.append(new_review)
        return new_review

    def delete_reviews(self, restaurant):
        self.reviews = [review for review in self.reviews if review.restaurant != restaurant]

    def __repr__(self):
        return f"<Customer(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    reviews = relationship('Review', back_populates='restaurant')

    def all_reviews(self):
        return [f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars."
                for review in self.reviews]

    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    star_rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

    def __repr__(self):
        return f"<Review(id={self.id}, content='{self.content}', star_rating={self.star_rating})>"

# Usage examples
# Create a new customer
new_customer = Customer(first_name='karanja', last_name='clair')
session.add(new_customer)
session.commit()

# Create a new restaurant
new_restaurant = Restaurant(name='sarova hotel', location='narok')
session.add(new_restaurant)
session.commit()

# Add a review
new_review = Review(content='Great food!', star_rating=5, customer=new_customer, restaurant=new_restaurant)
session.add(new_review)
session.commit()

# Retrieve all reviews for a restaurant
restaurant_reviews = session.query(Restaurant).filter_by(name='Sample Restaurant').first().all_reviews()
for review in restaurant_reviews:
    print(review)

# Find the fanciest restaurant
fanciest_restaurant = Restaurant.fanciest()
print(f"The fanciest restaurant is: {fanciest_restaurant.name} in {fanciest_restaurant.location}")
