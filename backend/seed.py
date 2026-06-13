from database import SessionLocal
from models import Prisoner
from face_recognition import get_embedding

db=SessionLocal()

embedding=get_embedding("uploads/prisoner1.jpg")
prisoner= Prisoner(
  full_name="Mike Le",
  age=22,
  gender="Male",
  description="thick eyebrows",
  last_seen_location="Mombasa",
  image_path="uploads/frowning.jpg",
  face_embedding=embedding
)
db.add(prisoner)
db.commit()
db.close()
print("Seed complete")