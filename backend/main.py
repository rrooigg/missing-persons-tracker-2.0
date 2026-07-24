import os
import gc
import shutil

# --- CRITICAL MEMORY OPTIMIZATIONS FOR RENDER FREE TIER ---
# Set these BEFORE importing tensorflow/deepface via face_recognition
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['MALLOC_TRIM_THRESHOLD_'] = '65536'

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Prisoner
from face_recognition import verify_faces

# Create database tables
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

# Add a Root Route so Render pings stop throwing 404 errors
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
        prisoners = db.query(Prisoner).all()
        
        match_found = False
        matched_prisoner = None
        final_distance = None

        for prisoner in prisoners:
            # Skip if the record doesn't have a valid image path to avoid system crashes
            if not prisoner.image_path or not os.path.exists(prisoner.image_path):
                continue
                
            try:
                verified, distance, threshold = verify_faces(file_path, prisoner.image_path)
                
                if verified:
                    match_found = True
                    matched_prisoner = prisoner
                    final_distance = float(distance)
                    break # Stop looping immediately once a match is found to conserve RAM!
            except Exception as face_err:
                print(f"Error checking face against prisoner ID {prisoner.id}: {face_err}")
                continue # Skip corrupt files gracefully without killing the server

        # Explicitly invoke the Python garbage collector right after the heavy loop blocks run
        gc.collect()

        if match_found:
            return {
                "match_found": True,
                "matched_id": matched_prisoner.id,
                "matched_name": matched_prisoner.full_name,
                "distance": final_distance
            }

        return {
            "match_found": False,
            "message": "No matching prisoner found"
        }

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

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)