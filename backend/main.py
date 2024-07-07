from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import models
from database import engine, SessionLocal, Base
from schema import UserBase, Token, TokenData, FeedbackRatingCreate, FeedbackRatingResponse, ItemCreate, ItemResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# Constants for JWT token creation
SECRET_KEY = "randomcode123testo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2PasswordBearer instance to use for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# CORS middleware configuration
origins = [
    "*",  # Replace with your frontend URL
    # Add more allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Add the methods your frontend uses
    allow_headers=["*"],  # Specify headers allowed for the request
)

@app.on_event("startup")
async def on_startup():
    """Create database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

def get_password_hash(password):
    """Return the hashed version of the given password."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verify if the given plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Get the current authenticated user based on the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(models.User).where(models.User.username == token_data.username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/user")
async def get_users(db: AsyncSession = Depends(get_db)):
    """Get a list of all users."""
    results = await db.execute(select(models.User))
    users = results.scalars().all()
    return {"users": users}

@app.post("/register")
async def register_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    result = await db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"id": new_user.id, "username": new_user.username}

@app.post("/token", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    result = await db.execute(select(models.User).where(models.User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.delete("/user/delete/me")
async def delete_user_me(current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Delete the current authenticated user."""
    await db.execute(delete(models.User).where(models.User.username == current_user.username))
    await db.commit()
    return {"message": f"User '{current_user.username}' successfully deleted"}

@app.post("/feedback", response_model=FeedbackRatingResponse)
async def create_feedback_rating(feedback_rating: FeedbackRatingCreate, current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Create a new feedback rating for an item."""
    result = await db.execute(select(models.FeedbackRating).where(models.FeedbackRating.user_id == current_user.id, models.FeedbackRating.item_id == feedback_rating.item_id))
    existing_rating = result.scalars().first()
    if existing_rating:
        raise HTTPException(status_code=400, detail="User has already rated this item")

    new_rating = models.FeedbackRating(
        user_id=current_user.id,
        item_id=feedback_rating.item_id,
        rating=feedback_rating.rating
    )

    db.add(new_rating)
    await db.commit()
    await db.refresh(new_rating)

    return FeedbackRatingResponse(id=new_rating.id, user_id=new_rating.user_id, item_id=new_rating.item_id, rating=new_rating.rating)

@app.get("/feedback/{item_id}", response_model=list[FeedbackRatingResponse])
async def get_feedback_ratings(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get all feedback ratings for a specific item."""
    result = await db.execute(select(models.FeedbackRating).where(models.FeedbackRating.item_id == item_id))
    ratings = result.scalars().all()
    return [FeedbackRatingResponse(id=rating.id, user_id=rating.user_id, item_id=rating.item_id, rating=rating.rating) for rating in ratings]

@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    """Create a new item."""
    result = await db.execute(select(models.Item).where(models.Item.title == item.title))
    existing_item = result.scalars().first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item with this title already exists")
    
    new_item = models.Item(title=item.title)
    
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    
    return new_item

@app.post("/clean", response_model=dict)
async def clean_all_tables(db: AsyncSession = Depends(get_db)):
    """Clean all tables by truncating them."""
    try:
        # Truncate all tables
        await db.execute(text("TRUNCATE TABLE users, items, feedback_ratings RESTART IDENTITY CASCADE"))
        await db.commit()
        return {"message": "All tables have been cleaned successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clean tables: {e}")
