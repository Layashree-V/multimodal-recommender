from app.database.connection import SessionLocal
from app.recommender.profile_builder import UserProfileBuilder

db = SessionLocal()

builder = UserProfileBuilder(db)

profile = builder.build_profile(user_id=1)

if profile:
    print("Embedding length:", len(profile))
    print(profile[:10])  # first 10 values
else:
    print("No interactions found.")

db.close()