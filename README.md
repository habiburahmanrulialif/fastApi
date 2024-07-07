# Feecback rating component
## Main idea
User would be able to rate the item or product provided to them.

## Documentation
FastAPI Application for User Management, Authentication, and Feedback Ratings
This FastAPI application provides endpoints for user registration, authentication, feedback ratings, and item management. The application uses SQLAlchemy for database interactions and JWT for authentication.


### API Endpoints

#### User Endpoints
- Get Users

URL: /user
Method: GET
Description: Retrieve a list of all registered users.
Response: JSON object containing a list of users.

- Register User

URL: /register
Method: POST
Description: Register a new user.
Request Body: UserBase (username, password)
Response: JSON object containing the new user's ID and username.

- Delete Current User

URL: /user/delete/me
Method: DELETE
Description: Delete the currently authenticated user.
Response: JSON object confirming the user deletion.

#### Authentication Endpoints
- Login for Access Token

> URL: /token
Method: POST
Description: Authenticate the user and return a JWT access token.
Request Body: OAuth2PasswordRequestForm (username, password)
Response: JSON object containing the access token and token type.

#### Feedback Rating Endpoints
- Create Feedback Rating

URL: /feedback
Method: POST
Description: Create a new feedback rating for an item.
Request Body: FeedbackRatingCreate (item_id, rating)
Response: JSON object containing the feedback rating details.

- Get Feedback Ratings

URL: /feedback/{item_id}
Method: GET
Description: Retrieve all feedback ratings for a specific item.
Response: JSON object containing a list of feedback ratings.

#### Item Endpoints
- Create Item

URL: /items
Method: POST
Description: Create a new item.
Request Body: ItemCreate (title)
Response: JSON object containing the item details.

#### Utility Endpoints
- Clean All Tables

URL: /clean
Method: POST
Description: Clean all tables by truncating them.
Response: JSON object confirming the tables have been cleaned.

### Database Models
- User
Fields: id, username, hashed_password

- FeedbackRating
Fields: id, user_id, item_id, rating

- Item
Fields: id, title

### Schemas
- UserBase
Fields: username, password

- Token
Fields: access_token, token_type, username

- TokenData
Fields: username

- FeedbackRatingCreate
Fields: item_id, rating

- FeedbackRatingResponse
Fields: id, user_id, item_id, rating

- ItemCreate
Fields: title

- ItemResponse
Fields: id, title

### Security
-Password Hashing
Passwords are hashed using the bcrypt algorithm for secure storage.

- JWT Authentication
JWT tokens are used for authenticating users. Tokens are created with a secret key and have an expiration time.

### CORS Configuration
- Origins
The application allows all origins (*) for CORS. You can restrict this to specific origins as needed.

- Allowed Methods
The application allows GET, POST, PUT, and DELETE methods. You can add or remove methods based on your requirements.

-Allowed Headers
The application allows all headers (*). You can specify which headers are allowed for the request.

## Setup 
> Python and [Git](https://git-scm.com) must be installed on your computer.  
> Creating a virtual environment is optional, but it is usually better to do so if you know how.
> [Postgresql](https://www.postgresql.org/download/) must be installed and running, and create database named : feedbackDb.
> [Docker](https://docs.docker.com/engine/install/) must be installed and running.

Install docker-compose
```
pip install docker-compose
```  
Build docker
```
docker-compose build
```  
Run docker
```
docker-compose up
```
