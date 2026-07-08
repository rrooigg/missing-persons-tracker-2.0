from database import SessionLocal
from models import Prisoner

db = SessionLocal()

prisoner = Prisoner(
  full_name="Mike Lee",
  age=22,
  gender="Female",
  description="thick eyebrows",
  last_seen_location="Mombasa",
  image_path="uploads/smiling.png",
 
)

db.add(prisoner)
db.commit()
db.close()

print("Seed complete")