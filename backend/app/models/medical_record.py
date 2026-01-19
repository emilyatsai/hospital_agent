from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class MedicalRecord(Base):
    """
    Medical record model for storing patient medical history and records
    """
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=False)

    # Record details
    record_type = Column(String, nullable=False)  # consultation, test_result, prescription, etc.
    record_date = Column(DateTime, default=datetime.utcnow)

    # Clinical information
    chief_complaint = Column(Text, nullable=True)
    history_of_present_illness = Column(Text, nullable=True)
    physical_examination = Column(Text, nullable=True)
    assessment = Column(Text, nullable=True)
    plan = Column(Text, nullable=True)

    # Vital signs
    blood_pressure_systolic = Column(Float, nullable=True)
    blood_pressure_diastolic = Column(Float, nullable=True)
    heart_rate = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    respiratory_rate = Column(Float, nullable=True)
    oxygen_saturation = Column(Float, nullable=True)

    # Laboratory results
    lab_results = Column(JSON, nullable=True)  # JSON object with test results

    # Prescriptions
    prescriptions = Column(JSON, nullable=True)  # JSON array of medications

    # Diagnosis
    diagnosis_codes = Column(JSON, nullable=True)  # ICD-10 codes
    diagnosis_descriptions = Column(JSON, nullable=True)

    # Follow-up information
    follow_up_instructions = Column(Text, nullable=True)
    next_appointment_date = Column(DateTime, nullable=True)

    # File attachments
    attachments = Column(JSON, nullable=True)  # JSON array of file paths/URLs

    # AI insights
    ai_summary = Column(Text, nullable=True)
    ai_recommendations = Column(Text, nullable=True)

    # Privacy and consent
    is_confidential = Column(Boolean, default=False)
    patient_consent_given = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("User", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")