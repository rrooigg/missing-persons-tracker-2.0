from database import SessionLocal
from models import Institution, Person


def seed_data():

    db = SessionLocal()

    try:

        # ---------------------------------------------
        # INSTITUTIONS
        # ---------------------------------------------

        institutions_data = [

            {
                "name": "Jela Baridi Prison",
                "institution_type": "Prison",
                "location": "Nairobi",
                "contact": "+254 700 000 001"
            },

            {
                "name": "Port Reitz Hospital",
                "institution_type": "Hospital",
                "location": "Mombasa",
                "contact": "+254 700 000 002"
            },

            {
                "name": "Mombasa Police Station",
                "institution_type": "Police",
                "location": "Mombasa",
                "contact": "+254 700 000 003"
            },

            {
                "name": "Mombasa Primary School",
                "institution_type": "School",
                "location": "Mombasa",
                "contact": "+254 700 000 004"
            },

            {
                "name": "Coast General Hospital",
                "institution_type": "Hospital",
                "location": "Mombasa",
                "contact": "+254 700 000 005"
            }

        ]


        institutions = {}


        for data in institutions_data:

            existing = (
                db.query(Institution)
                .filter(
                    Institution.name
                    == data["name"]
                )
                .first()
            )

            if existing:

                institution = existing

            else:

                institution = Institution(
                    name=data["name"],
                    institution_type=(
                        data["institution_type"]
                    ),
                    location=data["location"],
                    contact=data["contact"]
                )

                db.add(institution)
                db.commit()
                db.refresh(institution)


            institutions[
                data["name"]
            ] = institution


        # ---------------------------------------------
        # PEOPLE
        # ---------------------------------------------

        people_data = [

            {
                "full_name": "John Kamau",
                "age": 34,
                "gender": "Male",
                "description": (
                    "Medium height, short black hair, "
                    "small scar above left eyebrow."
                ),
                "last_seen_location": "Nairobi",
                "image_path": "uploads/prisoner2.jpg",
                "institution": "Jela Baridi Prison"
            },

            {
                "full_name": "Peter Otieno",
                "age": 29,
                "gender": "Male",
                "description": (
                    "Tall, dark complexion, "
                    "short hair."
                ),
                "last_seen_location": "Mombasa",
                "image_path": "uploads/smiling.png",
                "institution": "Jela Baridi Prison"
            },

            {
                "full_name": "Mary Achieng",
                "age": 24,
                "gender": "Female",
                "description": (
                    "Medium height, long black hair."
                ),
                "last_seen_location": "Mombasa",
                "image_path": "uploads/prisoner1.jpg",
                "institution": "Port Reitz Hospital"
            },

            {
                "full_name": "David Mwangi",
                "age": 41,
                "gender": "Male",
                "description": (
                    "Medium build, glasses, "
                    "short hair."
                ),
                "last_seen_location": "Mombasa",
                "image_path": "uploads/testing_young.jpg",
                "institution": "Mombasa Police Station"
            },

        ]


        for data in people_data:

            existing = (
                db.query(Person)
                .filter(
                    Person.full_name
                    == data["full_name"]
                )
                .first()
            )

            if existing:

                continue


            institution = institutions[
                data["institution"]
            ]


            person = Person(

                full_name=data["full_name"],

                age=data["age"],

                gender=data["gender"],

                description=data["description"],

                last_seen_location=(
                    data["last_seen_location"]
                ),

                image_path=data["image_path"],

                institution_id=institution.id

            )

            db.add(person)


        db.commit()

        print("Seed data inserted successfully.")


    finally:

        db.close()


if __name__ == "__main__":
    seed_data()