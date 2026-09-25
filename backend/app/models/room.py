from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    available_from = Column(String(5), nullable=False, default="09:00")  # HH:MM
    available_until = Column(String(5), nullable=False, default="13:00")  # HH:MM
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    schedule_entries = relationship("Schedule", back_populates="room", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}', hours='{self.available_from}-{self.available_until}')>"
