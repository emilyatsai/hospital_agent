from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentType(str, enum.Enum):
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"
    TELECONSULTATION = "teleconsultation"
    PROCEDURE = "procedure"


class Appointment(Base):
    """
    Appointment model for managing doctor-patient appointments
    """
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=False)

    appointment_type = Column(Enum(AppointmentType), default=AppointmentType.CONSULTATION)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)

    # Appointment details
    scheduled_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    actual_start_time = Column(DateTime, nullable=True)
    actual_end_time = Column(DateTime, nullable=True)

    # Location/Consultation details
    is_virtual = Column(Boolean, default=False)
    meeting_link = Column(String, nullable=True)
    location = Column(String, nullable=True)

    # Appointment information
    reason_for_visit = Column(Text, nullable=True)
    symptoms = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    # Billing
    consultation_fee = Column(Float, default=0.0)
    payment_status = Column(String, default="pending")  # pending, paid, refunded

    # Follow-up
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)

    # AI insights
    ai_risk_score = Column(Float, nullable=True)
    ai_recommendations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("User", back_populates="appointments", foreign_keys=[patient_id])
    doctor = relationship("Doctor", back_populates="appointments")