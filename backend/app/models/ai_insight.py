from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AIInsight(Base):
    """
    AI insight model for storing AI-generated medical insights and recommendations
    """
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Insight details
    insight_type = Column(String, nullable=False)  # diagnosis, treatment, risk_assessment, etc.
    insight_category = Column(String, nullable=True)  # cardiology, neurology, preventive_care, etc.

    # AI analysis input
    input_data = Column(JSON, nullable=True)  # JSON object with input data used for analysis
    analysis_date = Column(DateTime, default=datetime.utcnow)

    # AI-generated content
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    detailed_analysis = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True)  # JSON array of recommendations
    risk_score = Column(Float, nullable=True)  # 0-1 scale
    confidence_level = Column(Float, nullable=True)  # 0-1 scale

    # Medical insights
    predicted_conditions = Column(JSON, nullable=True)  # JSON array of predicted conditions
    treatment_suggestions = Column(JSON, nullable=True)  # JSON array of treatment suggestions
    preventive_measures = Column(JSON, nullable=True)  # JSON array of preventive measures
    medication_suggestions = Column(JSON, nullable=True)  # JSON array of medication suggestions

    # Evidence and sources
    evidence_sources = Column(JSON, nullable=True)  # JSON array of sources/references
    clinical_guidelines = Column(JSON, nullable=True)  # JSON array of relevant guidelines

    # Status and validation
    is_reviewed_by_doctor = Column(Boolean, default=False)
    doctor_feedback = Column(Text, nullable=True)
    is_implemented = Column(Boolean, default=False)
    implementation_notes = Column(Text, nullable=True)

    # Metadata
    ai_model_version = Column(String, nullable=True)
    processing_time_seconds = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("User", back_populates="ai_insights")