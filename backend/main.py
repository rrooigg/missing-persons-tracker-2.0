import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Prisoner
from face_recognition import verify_faces

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Missing Persons Tracker API")

# Enable CORS for local frontend development (e.g., React on localhost:3000 or 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images statically
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Missing Persons Tracker API is running locally."}

@app.post("/add-prisoner/")
async def add_prisoner(
    name: str = Form(...),
    age: int = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save the uploaded target image to local storage
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata to database
    new_prisoner = Prisoner(
        name=name,
        age=age,
        image_path=file_path
    )
    db.add(new_prisoner)
    db.commit()
    db.refresh(new_prisoner)

    return {"message": "Prisoner added successfully", "prisoner": new_prisoner}

@app.post("/search-prisoner/")
async def search_prisoner(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # 1. Save uploaded query image temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    query_img_path = os.path.join(temp_dir, file.filename)

    with open(query_img_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 2. Fetch all registered records
        prisoners = db.query(Prisoner).all()
        matched_prisoners = []

        # 3. Compare uploaded image against each stored record using verify()
        for prisoner in prisoners:
            if prisoner.image_path and os.path.exists(prisoner.image_path):
                is_match = verify_faces(query_img_path, prisoner.image_path)
                if is_match:
                    matched_prisoners.append(prisoner)

        return {"matches": matched_prisoners}

    finally:
        # Clean up temporary query image
        if os.path.exists(query_img_path):
            os.remove(query_img_path)

@app.get("/prisoner/{id}")
def get_prisoner(id: int, db: Session = Depends(get_db)):
    prisoner = db.query(Prisoner).filter(Prisoner.id == id).first()
    if not prisoner:
        raise HTTPException(status_code=404, detail="Prisoner not found")
    return prisoner