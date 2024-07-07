# Feecback rating component
## Main idea
User would be able to rate the item or product provided to them.

## Documentation
FastAPI Application for User Management, Authentication, and Feedback Ratings
This FastAPI application provides endpoints for user registration, authentication, feedback ratings, and item management. The application uses SQLAlchemy for database interactions and JWT for authentication.


### API Endpoints

#### User Endpoints
- Get Users
1. URL: /user
2. Method: GET
3. Description: Retrieve a list of all registered users.
4. Response: JSON object containing a list of users.
---
- Register User
1. URL: /register
2. Method: POST
3. Description: Register a new user.
4. Request Body: UserBase (username, password)
5. Response: JSON object containing the new user's ID and username.
---
- Delete Current User
1. URL: /user/delete/me
2. Method: DELETE
3. Description: Delete the currently authenticated user.
4. Response: JSON object confirming the user deletion.
---
#### Authentication Endpoints
- Login for Access Token
1. URL: /token
2. Method: POST
3. Description: Authenticate the user and return a JWT access token.
4. Request Body: OAuth2PasswordRequestForm (username, password)
5. Response: JSON object containing the access token and token type.
---
#### Feedback Rating Endpoints
- Create Feedback Rating
1. URL: /feedback
2. Method: POST
3. Description: Create a new feedback rating for an item.
4. Request Body: FeedbackRatingCreate (item_id, rating)
5. Response: JSON object containing the feedback rating details.
---
- Get Feedback Ratings
1. URL: /feedback/{item_id}
2. Method: GET
3. Description: Retrieve all feedback ratings for a specific item.
4. Response: JSON object containing a list of feedback ratings.
---
#### Item Endpoints
- Create Item
1. URL: /items
2. Method: POST
3. Description: Create a new item.
4. Request Body: ItemCreate (title)
5. Response: JSON object containing the item details.
---
#### Utility Endpoints
- Clean All Tables
1. URL: /clean
2. Method: POST
3. Description: Clean all tables by truncating them.
4. Response: JSON object confirming the tables have been cleaned.
---
### Database Models
- User
1. Fields: id, username, hashed_password
---
- FeedbackRating
1. Fields: id, user_id, item_id, rating
---
- Item
1. Fields: id, title
---
### Schemas
- UserBase
1. Fields: username, password
---
- Token
1. Fields: access_token, token_type, username
---
- TokenData
1. Fields: username
---
- FeedbackRatingCreate
1. Fields: item_id, rating
---
- FeedbackRatingResponse
1. Fields: id, user_id, item_id, rating
---
- ItemCreate
1. Fields: title
---
- ItemResponse
1. Fields: id, title
---
### Security
-Password Hashing
1. Passwords are hashed using the bcrypt algorithm for secure storage.
---
- JWT Authentication
1. JWT tokens are used for authenticating users. Tokens are created with a secret key and have an expiration time.
---
### CORS Configuration
- Origins
1. The application allows all origins (*) for CORS. You can restrict this to specific origins as needed.
---
- Allowed Methods
1. The application allows GET, POST, PUT, and DELETE methods. You can add or remove methods based on your requirements.
---
-Allowed Headers
1. The application allows all headers (*). You can specify which headers are allowed for the request.
---
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
Run the front end
```
npm run dev
```
