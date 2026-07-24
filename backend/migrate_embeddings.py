# migrate_embeddings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

# Now import database & models safely
from database import SessionLocal, engine
from models import Prisoner
from face_recognition import get_face_embedding
from sqlalchemy import text

def migrate():
    # Ensure extension exists
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()

    db = SessionLocal()
    try:
        prisoners = db.query(Prisoner).filter(Prisoner.embedding == None).all()
        print(f"Found {len(prisoners)} records needing embeddings...")

        for p in prisoners:
            if not p.image_path or not os.path.exists(p.image_path):
                print(f"⚠️ Skipping ID {p.id} ({p.full_name}): Image file not found at '{p.image_path}'")
                continue

            print(f"Processing ID {p.id} ({p.full_name})...")
            vec = get_face_embedding(p.image_path)

            if vec:
                p.embedding = vec
                db.commit()
                print(f"✅ Updated embedding for ID {p.id}")
            else:
                print(f"❌ Could not detect face for ID {p.id}")

        print("\n🎉 Migration finished!")
    finally:
        db.close()

if __name__ == "__main__":
    migrate()