from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentType(str, Enum):
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"
    TELECONSULTATION = "teleconsultation"
    PROCEDURE = "procedure"


class AppointmentBase(BaseModel):
    doctor_id: int
    appointment_type: AppointmentType = AppointmentType.CONSULTATION
    scheduled_date: datetime
    duration_minutes: int = 30
    is_virtual: bool = False
    reason_for_visit: Optional[str] = None
    symptoms: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    scheduled_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    is_virtual: Optional[bool] = None
    reason_for_visit: Optional[str] = None
    symptoms: Optional[str] = None
    notes: Optional[str] = None
    meeting_link: Optional[str] = None
    location: Optional[str] = None


class AppointmentInDBBase(AppointmentBase):
    id: int
    patient_id: int
    status: AppointmentStatus
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    meeting_link: Optional[str] = None
    location: Optional[str] = None
    consultation_fee: float
    payment_status: str
    follow_up_required: bool
    follow_up_date: Optional[datetime] = None
    ai_risk_score: Optional[float] = None
    ai_recommendations: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Appointment(AppointmentInDBBase):
    pass