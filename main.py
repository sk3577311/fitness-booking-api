from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
import models, schemas
from database import SessionLocal, engine
from datetime import datetime
import pytz
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

IST = pytz.timezone("Asia/Kolkata")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Seed classes
@app.on_event("startup")
def seed_data():
    db = next(get_db())
    if db.query(models.FitnessClass).count() == 0:
        now = datetime.now(IST)
        classes = [
            models.FitnessClass(name="Yoga", datetime=now, instructor="Rita", available_slots=10),
            models.FitnessClass(name="Zumba", datetime=now.replace(hour=18), instructor="Raj", available_slots=8),
            models.FitnessClass(name="HIIT", datetime=now.replace(hour=20), instructor="Sam", available_slots=5),
        ]
        db.add_all(classes)
        db.commit()

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request, db: Session = Depends(get_db)):
    classes = db.query(models.FitnessClass).all()
    return templates.TemplateResponse("index.html", {"request": request, "classes": classes})

@app.get("/book", response_class=HTMLResponse)
def book_page(request: Request, db: Session = Depends(get_db)):
    classes = db.query(models.FitnessClass).all()
    return templates.TemplateResponse("book.html", {"request": request, "classes": classes})

@app.post("/book", response_class=HTMLResponse)
def book_class(
    request: Request,
    class_id: int = Form(...),
    client_name: str = Form(...),
    client_email: str = Form(...),
    db: Session = Depends(get_db)
):
    cls = db.query(models.FitnessClass).filter_by(id=class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    if cls.available_slots < 1:
        raise HTTPException(status_code=400, detail="No available slots")

    cls.available_slots -= 1
    booking = models.Booking(class_id=class_id, client_name=client_name, client_email=client_email)
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return templates.TemplateResponse("bookings.html", {"request": request, "bookings": [booking]})

@app.get("/bookings", response_class=HTMLResponse)
def view_bookings(request: Request, email: str, db: Session = Depends(get_db)):
    db = SessionLocal()
    bookings = db.query(models.Booking).filter_by(client_email=email).all()
    return templates.TemplateResponse("bookings.html", {"request": request, "bookings": bookings})

@app.get("/classes", response_model=list[schemas.FitnessClassOut])
def api_classes(db: Session = Depends(get_db)):
    return db.query(models.FitnessClass).all()

@app.post("/api/book", response_model=schemas.BookingOut)
def api_book(booking: schemas.BookingRequest, db: Session = Depends(get_db)):
    cls = db.query(models.FitnessClass).filter_by(id=booking.class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    if cls.available_slots < 1:
        raise HTTPException(status_code=400, detail="No slots left")
    cls.available_slots -= 1
    new_booking = models.Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/api/bookings", response_model=list[schemas.BookingOut])
def api_get_bookings(email: str, db: Session = Depends(get_db)):
    return db.query(models.Booking).filter_by(client_email=email).all()

def init_db():
    models.Base.metadata.create_all(bind=engine)

    # Load seed data if DB is empty
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM classes")
    count = cursor.fetchone()[0]

    if count == 0:
        with open("seed.sql", "r") as f:
            cursor.executescript(f.read())
        conn.commit()

    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()