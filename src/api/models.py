from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Text, DateTime, Integer
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

    behavior_analyses: Mapped[List["BehaviorAnalysis"]] = relationship(
        back_populates="user"
    )

    scenario_answers: Mapped[List["ScenarioAnswer"]] = relationship(
        back_populates="user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "age": self.age,
        }


class Scenario(db.Model):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    correct_reflection: Mapped[str] = mapped_column(Text, nullable=False)

    answers: Mapped[List["ScenarioAnswer"]] = relationship(
        back_populates="scenario"
    )

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "correct_reflection": self.correct_reflection,
        }


class ScenarioAnswer(db.Model):
    __tablename__ = "scenario_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="scenario_answers")
    scenario: Mapped["Scenario"] = relationship(back_populates="answers")

    def serialize(self):
        return {
            "id": self.id,
            "answer": self.answer,
            "feedback": self.feedback,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "scenario_id": self.scenario_id,
        }


class BehaviorAnalysis(db.Model):
    __tablename__ = "behavior_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    behavior_text: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
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
            "user_id": self.user_id,
        }