from database import SessionLocal
from models import FitnessClass
from uuid import uuid4
from datetime import datetime
import pytz

db = SessionLocal()

classes = [
    FitnessClass(
        id=str(uuid4()),
        name="Yoga",
        datetime=pytz.timezone("Asia/Kolkata").localize(datetime(2025, 6, 15, 9, 0)),
        instructor="Alice",
        available_slots=5
    ),
    FitnessClass(
        id=str(uuid4()),
        name="Zumba",
        datetime=pytz.timezone("Asia/Kolkata").localize(datetime(2025, 6, 15, 11, 0)),
        instructor="Bob",
        available_slots=3
    ),
]

db.add_all(classes)
db.commit()
print("Seeded initial class data.")
