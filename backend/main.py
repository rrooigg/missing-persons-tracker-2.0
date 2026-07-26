from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from database import engine, SessionLocal
from models import Base, Prisoner
from face_recognition import verify_faces

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_prisoner(
    fullName: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    description: str = Form(...),
    lastSeenLocation: str = Form(...),
    file: UploadFile = File(...)
):
  
  file_path = f"{UPLOAD_DIR}/{file.filename}"

  with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  db: Session = SessionLocal()

  try:
    prisoners = db.query(Prisoner).all()
    best_match = None
    best_distance = float("inf")

    for prisoner in prisoners:
      try:
        verified, distance, threshold = verify_faces(
          file_path,
          prisoner.image_path
        )

        print("--------------------------")
        print("Prisoner:", prisoner.full_name)
        print("Verified:", verified)
        print("Distance:", distance)
        print("Threshold:", threshold)

        if verified and distance < best_distance:
          best_distance = distance
          best_match = prisoner

      except Exception as e:
        print("Verification error:", e)

    if best_match:
      return {
        "match_found": True,
        "matched_id": best_match.id,
        "matched_name": best_match.full_name,
        "distance": float(best_distance)
      }

    return {
      "match_found": False,
      "message": "No matching prisoner found"
    }

  finally:
    db.close()

@app.get("/prisoner/{prisoner_id}")
def get_prisoner(prisoner_id: int):
  db = SessionLocal()

  try:
    prisoner = (
       db.query(Prisoner)
      .filter(Prisoner.id == prisoner_id)
      .first()
    )

    if not prisoner:
      return {"message":"Not found"}
 
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