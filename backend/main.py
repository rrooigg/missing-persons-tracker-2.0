from fastapi import (
  FastAPI,
  UploadFile,
  File, 
  Form,
  HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, SessionLocal
from models import Base, Person, Institution
from face_recognition import verify_faces

#database
Base.metadata.create_all(bind=engine)

#app
app=FastAPI(
  title="Missing Persons Tracker API",
  version="1.0.0"
)

#cors
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

#upload directory
UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount(
  "/uploads",
  StaticFiles(directory=UPLOAD_DIR),
  name="uploads"
)
#root
@app.get("/")
def root():
  return {
    "message":"Missing Persons Tracker API is running"
  }

#institutions
@app.get("/institutions")
def get_institutions():
  db:Session=SessionLocal()

  try:
    institutions=(
      db.query(Institution)
      .order_by(Institution.name)
      .all()
    )
    result=[]

    for institution in institutions:
      people_count=(
        db.query(Person)
        .filter(
          Person.institution_id == institution.id
        )
        .count
      )
      result.append({
        "id":institution.id,
        "name": institution.name,
        "institution_type":institution.institution_type,
        "location":institution.location,
        "contact":institution.contact,
        "people_count":people_count
      })

    return result

  finally:
    db.close()

#register institution
@app.post("/institutions")
def create_institution(
  name:str=Form(...),
  institution_type:str=Form(...),
  location:str=Form(...),
  contact:str=Form("")
):
  db:Session=SessionLocal()

  try:
    existing=(
      db.query(Institution)
      .filter(Institution.name == name)
      .first()
    )
    if existing:
      raise HTTPException(
        status_code=400,
        detail="Institution already exists"
      )
    institution=Institution(
      name=name,
      institution_type=institution_type,
      location=location,
      contact=contact
    )
    db.add(institution)
    db.commit()
    db.refresh(institution)

    return {
      "message":"Institution registered successfully",
      "institution":{
        "id":institution.id,
        "name":institution.name,
        "institution_type":institution.institution_type,
        "location":institution.location,
        "contact":institution.contact
      }
    }
  finally:
    db.close()

#search
@app.post("/upload")
async def upload_person(
  fullName:str=Form(...),
  age:int=Form(...),
  gender:str=Form(...),
  description:str=Form(...),
  lastSeenLocation:str=Form(...),
  file:UploadFile=File(...)
):
  if not file.content_type:
    raise HTTPException(
      status_code=400,
      detail="File type could not be determined"
    )
  if not file.content_type.startswith("image/"):
    raise HTTPException(
      status_code=400,
      detail="Please upload an image"
    )
  #save uploaded image
  extension=os.path.splitext(file.filename)[1]

  unique_filename=(
    f"{uuid.uuid4().hex}{extension}"
  )
  file_path=os.path.join(
    UPLOAD_DIR,
    unique_filename
  )
  with open(file_path, "wb") as buffer:
    shutil.copyfileobj(
      file.file,
      buffer
    )

  #db
  db:Session=SessionLocal()
  try:
    people=(
      db.query(Person)
      .all()
    )
    best_match=None
    best_distance=float("inf")
    best_threshold=None

    #save every person
    for person in people:
      if not person.image_path:
        continue
      stored_path=person.image_path

      if not os.path.exists(stored_path):
        print(
          f"Image missing for {person.full_name}:"
          f"{stored_path}"
        )
        continue

      try:
        verified, distance, threshold=verify_faces(
          file_path,
          stored_path
        )
        print("----------------")
        print(
          "Person:",
          person.full_name
        )
        print(
          "Institution:",
          person.institution.name
        )
        print(
          "Verified:",
          verified
        )
        print(
          "Distance:",
          distance
        )
        print(
          "Threshold:",
          threshold
        )

        if(
          verified
          and distance<best_distance
        ):
          best_distance=distance
          best_match=person
          best_threshold=threshold
      except Exception as e:
        print(
          f"Verification error for"
          f"{person.full_name}:{e}"
        )
    #match found
    if best_match:
      institution=(
        db.query(Institution)
        .filter(
          Institution.id==best_match.institution_id
        )
        .first()
      )

      return {
        "match_found":True,
        "matched_id":best_match.id,
        "matched_name":best_match.full_name,
        "distance": floar(
          best_distance
        ),
        "threshold": float(
          best_threshold
        ) if best_threshold is not None else None,

        "institution": {
          "id":institution.id,
          "name":institution.name,
          "type":institution.institution_type,
          "location":institution.location
        }
      }
    #no match
    return {
      "match_found":False,
      "message":"No matching record found"
    }
  finally:
    db.close()

#person details
@app.get("/person/{person_id}")
def get_person(person_id:int):
  db:Session=SessionLocal()

  try:
    person=(
      db.query(Person)
      .filter(Person.id==person_id)
      .first()
    )
    if not person:
      raise HTTPException(
        status_code=404,
        detail="Person not found"
      )
    institution=(
      db.query(Institution)
      .filter(
        Institution.id==person.institution_id
      )
      .first()
    )

    return {
      "id":person.id,
      "full_name":person.full_name,
      "age":person.age,
      "gender":person.gender,
      "description":person.description,
      "last_seen_location": (
        person.last_seen_location
      ),
      "image_path":person.image_path,
      "institution":  {
        "id":institution.id,
        "name":institution.name,
        "type": (institution.institution_type),
        "location":institution.location,
        "contact":institution.contact
      }
    }
  finally:
    db.close()

#dashboard statistics
@app.get("/dashboard/stats")
def dashboard_stats():
  db:Session=SessionLocal()

  try:
    institutions_count=(
      db.query(Institution)
      .count()
    )
    people_count=(
      db.query(Person)
      .count()
    )
    institution_counts=(
      db.query(
        Institution.institution_type,
        func.count(Person.id)
      )
      .outerjoin(
        Person,
        Person.institution_id==Institution.id
      )
      .group_by(
        Institution.institution_type
      )
      .all()
    )

    by_type={}
    for institution_type, count in institution_counts:
      by_type[institution_type] = count

    return {
      "institutions_count": institutions_count,
      "people_count": people_count,
      "by_type":by_type
    }
  finally:
    db.close()