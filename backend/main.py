from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware #controls which websites(frontend) has access to backend
import shutil #to save uploaded files
import os #works with files/folders
from sqlalchemy.orm import Session


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

  #create prisoner object
  new_prisoner = Prisoner(
    full_name = fullName,
    age=age,
    gender=gender,
    description=description,
    last_seen_location=lastSeenLocation,
    image_path=file_path

  )
  #save to DB
  db.add(new_prisoner)
  db.commit() #permanently saves it to db
  db.refresh(new_prisoner) #return fully updated obj 

  db.close()

  return {
    "message": "Uploaded successfully",
    "id": new_prisoner.id
  }