from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.appointment import Appointment
from app.schemas.appointment import Appointment as AppointmentSchema, AppointmentCreate, AppointmentUpdate

router = APIRouter()


@router.get("/", response_model=List[AppointmentSchema])
def read_appointments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve appointments for current user
    """
    if current_user.role == "doctor":
        appointments = db.query(Appointment).filter(
            Appointment.doctor_id == current_user.doctor_profile.id if hasattr(current_user, 'doctor_profile') else False
        ).offset(skip).limit(limit).all()
    else:
        appointments = db.query(Appointment).filter(
            Appointment.patient_id == current_user.id
        ).offset(skip).limit(limit).all()
    return appointments


@router.post("/", response_model=AppointmentSchema)
def create_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_in: AppointmentCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new appointment
    """
    appointment = Appointment(
        **appointment_in.model_dump(),
        patient_id=current_user.id
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/{appointment_id}", response_model=AppointmentSchema)
def read_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get appointment by ID
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    # Check if user has permission to view this appointment
    if (appointment.patient_id != current_user.id and
        (not hasattr(current_user, 'doctor_profile') or
         current_user.doctor_profile.id != appointment.doctor_id) and
        not current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentSchema)
def update_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update appointment
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    # Check permissions
    if (appointment.patient_id != current_user.id and
        (not hasattr(current_user, 'doctor_profile') or
         current_user.doctor_profile.id != appointment.doctor_id) and
        not current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    for field, value in appointment_in.model_dump(exclude_unset=True).items():
        setattr(appointment, field, value)

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete appointment
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    # Check permissions (only patient or admin can delete)
    if appointment.patient_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}