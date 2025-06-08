import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User  # adjust import if needed
from app.core.config import settings

DATABASE_URL = str(settings.database_uri)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed_users():
    session = SessionLocal()
    try:
        users = [
            User(
                id=uuid.uuid4(),
                full_name="Alice Example",
                username="alice",
                password="hashed_password1",  
                email="alice@example.com",
            ),
            User(
                id=uuid.uuid4(),
                full_name="Bob Example",
                username="bob",
                password="hashed_password2",
                email="bob@example.com",
            ),
            User(
                id=uuid.uuid4(),
                full_name="Charlie Example",
                username="charlie",
                password="hashed_password3",
                email="charlie@example.com",
            ),
        ]
        session.add_all(users)
        session.commit()
        print("Seeded users successfully!")
    except Exception as e:
        session.rollback()
        print("Error seeding users:", e)
    finally:
        session.close()


if __name__ == "__main__":
    seed_users()
