from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    behavior_analyses: Mapped[list["BehaviorAnalysis"]] = relationship(
        back_populates="user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "age": self.age,
            "is_active": self.is_active
        }

class BehaviorAnalysis(db.Model):
    __tablename__ = "behavior_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    behavior_text: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(30), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="behavior_analyses")

    def serialize(self):
        return {
            "id": self.id,
            "behavior_text": self.behavior_text,
            "risk_level": self.risk_level,
            "category": self.category,
            "feedback": self.feedback,
            "recommendation": self.recommendation,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }
