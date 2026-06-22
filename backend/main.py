from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware #controls which websites(frontend) has access to backend
import shutil #to save uploaded files
import os #works with files/folders
from sqlalchemy.orm import Session
from face_recognition import get_embedding, find_best_match
from fastapi.staticfiles import StaticFiles 

from database import engine, SessionLocal
from models import Base, Prisoner 
#automatically create table in postgresql
Base.metadata.create_all(bind=engine)

app = FastAPI() #creates backend application
app.add_middleware(
  CORSMiddleware, #adss CORS
  allow_origins=["http://localhost:5173"], #only this frontend URL is allowed
  allow_credentials=True, #allows cookies/authentication data to be shared
  allow_methods=["*"], #allows all HTTP methods
  allow_headers=["*"], #allows frontend to send headers i.e JSON
) 
#create folder wwhere files(images) will be uploaded
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  #if it exists don't crash 

#if POST request is sent to "/upload", run function below
@app.post("/upload") #to send data
#receives sent data from frontend(react)
async def upload_prisoner(
  fullName: str = Form(...), #Form(...) shows this is from form data and not JSON, ... means 'required/must answer'
  age: int = Form(...),
  gender: str = Form(...),
  description: str = Form(...),
  lastSeenLocation: str = Form(...),
  file: UploadFile = File(...) #shows this is a file upload
):
  #save uploaded file 
  file_path = f"{UPLOAD_DIR}/{file.filename}"

  with open(file_path, "wb") as buffer: #opens file in binary-mode(isn't human-readable)
    shutil.copyfileobj(file.file, buffer) #copies uploaded file into folder
  
  #connect to DB
  db: Session = SessionLocal()

  try:
    #Extract face embedding
    try:
      uploaded_embedding=get_embedding(file_path)
    
    except Exception:
      return {
        "message": "No face detected in uploaded image"
      }
    
    #Search for existing prisoner
    prisoners=db.query(Prisoner).all()

    best_match, similarity=find_best_match(
      uploaded_embedding,
      prisoners
    )
    #debugging
    print("Best Match: ", best_match.full_name if best_match else None)
    print("Similarity: ", similarity)
    
    #Threshold
    if best_match and similarity > 0.80:
      return {
        "match_found":True,
        "matched_id":best_match.id,
        "matched_name":best_match.full_name,
        "similarity":float(similarity),
        
      }
    return {
      "match_found":False,
      "message":"No matching prisoner found"

    }
  
  finally:
    db.close()

#add route to get prisoner details
@app.get("/prisoner/{prisoner_id}")
def get_prisoner(prisoner_id:int):
  db=SessionLocal()

  try:
    prisoner = (
      db.query(Prisoner)
      .filter(Prisoner.id == prisoner_id)
      .first()
    )

    if not prisoner:
      return {"message":"Not found"}
    
    return {
      "id":prisoner_id,
      "full_name":prisoner.full_name,
      "age":prisoner.age,
      "gender":prisoner.gender,
      "description":prisoner.description,
      "last_seen_location":prisoner.last_seen_location,
      "image_path":prisoner.image_path
    }
  finally:
    db.close()

app.mount(
  "/uploads",
  StaticFiles(directory="uploads"),
  name="uploads"
)