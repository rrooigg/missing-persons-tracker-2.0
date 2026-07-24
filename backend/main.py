import os
import gc
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['MALLOC_TRIM_THRESHOLD_'] = '65536'

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import engine, SessionLocal
from models import Base, Prisoner
from face_recognition import get_face_embedding

# Enable pgvector on Neon DB
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://missing-persons-tracker.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Facenet distance threshold for verification (~0.40 to 0.55 depending on distance metric)
FACENET_THRESHOLD = 0.40 

@app.get("/")
def root():
    return {"status": "healthy", "service": "Missing Persons Tracker API"}

@app.post("/upload")
async def upload_prisoner(
    fullName: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    description: str = Form(...),
    lastSeenLocation: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db: Session = SessionLocal()

    try:
        # Step 1: Extract embedding ONCE for the uploaded image
        query_vector = get_face_embedding(file_path)

        if query_vector is None:
            raise HTTPException(status_code=400, detail="Could not process face from image.")

        # Step 2: Let Neon Postgres/pgvector do the search instantly in SQL
        # Using L2 distance (<->)
        nearest = (
            db.query(
                Prisoner,
                Prisoner.embedding.l2_distance(query_vector).label("distance")
            )
            .order_by("distance")
            .first()
        )

        # Step 3: Check distance against threshold
        if nearest:
            matched_prisoner, distance = nearest
            if distance is not None and distance <= FACENET_THRESHOLD:
                return {
                    "match_found": True,
                    "matched_id": matched_prisoner.id,
                    "matched_name": matched_prisoner.full_name,
                    "distance": float(distance)
                }

        # If no match found, save new record with its embedding
        new_prisoner = Prisoner(
            full_name=fullName,
            age=age,
            gender=gender,
            description=description,
            last_seen_location=lastSeenLocation,
            image_path=file_path,
            embedding=query_vector
        )
        db.add(new_prisoner)
        db.commit()

        return {
            "match_found": False,
            "message": "No matching prisoner found. Created new entry."
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"System processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal facial recognition server error")
        
    finally:
        db.close()

@app.get("/prisoner/{prisoner_id}")
def get_prisoner(prisoner_id: int):
    db = SessionLocal()
    try:
        prisoner = db.query(Prisoner).filter(Prisoner.id == prisoner_id).first()
        if not prisoner:
            return {"message": "Not found"}

        return {
            "id": prisoner.id,
            "full_name": prisoner.full_name,
            "age": prisoner.age,
            "gender": prisoner.gender,
            "description": prisoner.description,
            "last_seen_location": prisoner.last_seen_location,
            "image_path": prisoner.image_path
        }
    finally:
        db.close()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")