from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Doctor(Base):
    """
    Doctor model for healthcare professionals
    """
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    specialization = Column(String, nullable=False)
    qualifications = Column(Text, nullable=True)
    experience_years = Column(Integer, default=0)
    consultation_fee = Column(Float, default=0.0)
    available_days = Column(String, nullable=True)  # JSON string of available days
    available_hours_start = Column(String, nullable=True)  # e.g., "09:00"
    available_hours_end = Column(String, nullable=True)    # e.g., "17:00"
    is_available = Column(Boolean, default=True)
    hospital_department = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    languages_spoken = Column(String, nullable=True)  # JSON string of languages
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="doctor_profile")
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")