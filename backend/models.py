from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    feedbacks: Mapped[list["FeedbackRating"]] = relationship("FeedbackRating", back_populates="user")

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    ratings: Mapped[list["FeedbackRating"]] = relationship("FeedbackRating", back_populates="item")

class FeedbackRating(Base):
    __tablename__ = "feedback_ratings"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    rating: Mapped[int] = mapped_column()
    user: Mapped["User"] = relationship("User", back_populates="feedbacks")
    item: Mapped["Item"] = relationship("Item", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="unique_user_item"),
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range')
    )