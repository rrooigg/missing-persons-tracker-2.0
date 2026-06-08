from database import SessionLocal
from models import Prisoner
from face_recognition import get_embedding

db=SessionLocal()

embedding=get_embedding("uploads/prisoner1.jpg")
prisoner= Prisoner(
  full_name="John Doe",
  age=35,
  gender="Male",
  description="Scar on left cheek",
  last_seen_location="Mombasa",
  image_path="uploads/prisoner1.jpg",
  face_embedding=embedding
)
db.add(prisoner)
db.commit()
db.close()
print("Seed complete")