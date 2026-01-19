from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Patient(Base):
    """
    Extended patient information model
    """
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Medical Information
    blood_type = Column(String, nullable=True)
    allergies = Column(Text, nullable=True)  # JSON string of allergies
    chronic_conditions = Column(Text, nullable=True)  # JSON string of conditions
    medications = Column(Text, nullable=True)  # JSON string of current medications
    medical_history = Column(Text, nullable=True)  # JSON string of medical history

    # Insurance Information
    insurance_provider = Column(String, nullable=True)
    insurance_policy_number = Column(String, nullable=True)
    insurance_group_number = Column(String, nullable=True)

    # Emergency Contact
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relationship = Column(String, nullable=True)

    # Preferences
    preferred_language = Column(String, default="English")
    communication_preferences = Column(String, nullable=True)  # JSON string

    # Medical Metrics
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")
    ai_insights = relationship("AIInsight", back_populates="patient")