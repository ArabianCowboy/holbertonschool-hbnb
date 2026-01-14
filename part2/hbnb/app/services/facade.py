from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository() # Initialize the user repository
        self.place_repo = InMemoryRepository() # Initialize the place repository
        self.review_repo = InMemoryRepository() # Initialize the review repository
        self.amenity_repo = InMemoryRepository() # Initialize the amenity repository

    def create_user(self, user_data): # Create a new user and add it to the repository
        user = User(**user_data) # Create a new user object
        self.user_repo.add(user) # Add the user to the repository
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id) # Get a user by ID from the repository and return it
    
    def get_all_users(self):
        return self.user_repo.get_all() # Get all users from the repository and return them

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            self.user_repo.update(user_id, user_data) # Update a user by ID
        return user

    def get_user_by_email(self, email): # Get a user by email from the repository
        return self.user_repo.get_by_attribute('email', email)

    def get_place(self, place_id): # Get a place by ID from the repository

        return self.place_repo.get(place_id)