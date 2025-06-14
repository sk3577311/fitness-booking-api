from sqlalchemy.orm import Session
import models, schemas
from uuid import uuid4
from datetime import datetime
import pytz
from utils import convert_to_ist

def get_all_classes(db: Session):
    return db.query(models.FitnessClass).all()

def get_class_by_id(db: Session, class_id: str):
    return db.query(models.FitnessClass).filter(models.FitnessClass.id == class_id).first()

def book_class(db: Session, request: schemas.BookingRequest):
    fitness_class = get_class_by_id(db, request.class_id)
    if not fitness_class:
        raise ValueError("Class not found.")
    if fitness_class.available_slots <= 0:
        raise ValueError("No slots available.")

    fitness_class.available_slots -= 1
    db.add(fitness_class)

    booking = models.Booking(
        id=str(uuid4()),
        class_id=fitness_class.id,
        class_name=fitness_class.name,
        client_name=request.client_name,
        client_email=request.client_email,
        booked_at=convert_to_ist(datetime.utcnow())
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_bookings_by_email(db: Session, email: str):
    return db.query(models.Booking).filter(models.Booking.client_email == email).all()
