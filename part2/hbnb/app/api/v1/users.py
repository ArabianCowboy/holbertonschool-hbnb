from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations') # namespace for user operations to group related resources this is for flask restx

user_model = api.model('User', { # model to validate user data
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/') # route to create a new user and add it to the repository
class UserList(Resource): # class to handle user list resource  
    @api.expect(user_model, validate=True) # expect user data to be validated
    @api.response(201, 'User successfully created') # response if user is created successfully
    @api.response(400, 'Email already exists') # response if email already exists
    @api.response(400, 'Invalid input data') # response if input data is invalid
    def post(self):
        """ Register a new user """
        user_data = api.payload # get the user data from the request
        
        existing_user = facade.get_user_by_email(user_data['email']) # check if the user already exists
        if existing_user:
            return {'error': 'Email already registered'}, 400 # return error if the user already exists

        new_user = facade.create_user(user_data) # create the user  
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """ Get a list of all users"""
        users = facade.get_all_users() # get all users from the repository and return them
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200

        
@api.route('/<user_id>') # route to get a user by id 
class UserResource(Resource): # class to handle user resource
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id) # get user by id from the repository and return it
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True) # expect user data to be validated
    @api.response(200, 'User successfully updated') # response if user is updated successfully
    @api.response(404, 'User not found') # response if user is not found
    @api.response(400, 'Invalid input data') # response if input data is invalid
    def put(self, user_id): # update a user by id and return the updated user 
        """Update user information"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404 # return error if user is not found
        updated_user = facade.update_user(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
