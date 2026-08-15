import os
import sys
import random
from datetime import datetime, timedelta

# --------------------------------------------------
# Add backend directory to Python path
# --------------------------------------------------

BACKEND_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BACKEND_DIR)

# --------------------------------------------------
# Import database
# --------------------------------------------------

from app.database.connection import (
    SessionLocal,
    engine,
    Base
)

# --------------------------------------------------
# Import models
# --------------------------------------------------

from app.models.user import User
from app.models.content import Content
from app.models.interaction import Interaction


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

print("======================================")
print("INITIALIZING DATABASE")
print("======================================")

Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("Database initialized successfully.")


# ==================================================
# LOAD USERS
# ==================================================

users = db.query(User).all()

print()
print("======================================")
print("USERS")
print("======================================")

print(f"Users found : {len(users)}")

if not users:
    print("No users found.")
    print("Create at least one user first.")

    db.close()
    raise SystemExit


# ==================================================
# LOAD CONTENT
# ==================================================

contents = db.query(Content).all()

print()
print("======================================")
print("CONTENT")
print("======================================")

print(f"Content found : {len(contents)}")

if not contents:
    print("No content found.")
    print("Add content before generating interactions.")

    db.close()
    raise SystemExit


# ==================================================
# CONFIGURATION
# ==================================================

# Number of synthetic interactions to generate
NUM_INTERACTIONS = 1000

# Prevent duplicate interaction between
# same user and same content
ALLOW_DUPLICATES = False


# ==================================================
# EXISTING INTERACTIONS
# ==================================================

existing_pairs = set()

if not ALLOW_DUPLICATES:

    existing_interactions = (
        db.query(
            Interaction.user_id,
            Interaction.content_id
        )
        .all()
    )

    existing_pairs = {
        (user_id, content_id)
        for user_id, content_id
        in existing_interactions
    }

print()
print("Existing interactions :", len(existing_pairs))


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def generate_interaction():

    # ----------------------------------------------
    # Random engagement pattern
    # ----------------------------------------------

    clicked = random.random() < 0.75

    # Likes are more likely after clicking
    liked = (
        clicked
        and random.random() < 0.35
    )

    # Saves are less frequent
    saved = (
        clicked
        and random.random() < 0.18
    )

    # Shares are relatively rare
    shared = (
        clicked
        and random.random() < 0.10
    )

    # ----------------------------------------------
    # Watch time
    # ----------------------------------------------

    if clicked:

        watch_time = random.randint(
            10,
            600
        )

    else:

        watch_time = 0

    # ----------------------------------------------
    # Read time
    # ----------------------------------------------

    if clicked:

        read_time = random.randint(
            5,
            500
        )

    else:

        read_time = 0

    # ----------------------------------------------
    # Scroll depth
    #
    # 0.0 = didn't scroll
    # 1.0 = reached bottom
    # ----------------------------------------------

    if clicked:

        scroll_depth = round(
            random.uniform(
                0.05,
                1.0
            ),
            2
        )

    else:

        scroll_depth = 0.0

    return (
        clicked,
        liked,
        saved,
        shared,
        watch_time,
        read_time,
        scroll_depth
    )


# ==================================================
# GENERATE INTERACTIONS
# ==================================================

print()
print("======================================")
print("GENERATING SYNTHETIC INTERACTIONS")
print("======================================")

created = 0

attempts = 0

max_attempts = NUM_INTERACTIONS * 20


while created < NUM_INTERACTIONS:

    attempts += 1

    if attempts > max_attempts:

        print()
        print(
            "Could not generate the requested "
            "number of unique interactions."
        )

        break

    # ----------------------------------------------
    # Random user
    # ----------------------------------------------

    user = random.choice(users)

    # ----------------------------------------------
    # Random content
    # ----------------------------------------------

    content = random.choice(contents)

    pair = (
        user.id,
        content.id
    )

    # ----------------------------------------------
    # Avoid duplicates
    # ----------------------------------------------

    if not ALLOW_DUPLICATES:

        if pair in existing_pairs:

            continue

    # ----------------------------------------------
    # Generate behavior
    # ----------------------------------------------

    (
        clicked,
        liked,
        saved,
        shared,
        watch_time,
        read_time,
        scroll_depth
    ) = generate_interaction()

    # ----------------------------------------------
    # Random interaction time
    #
    # Generates activity over the last 90 days.
    # ----------------------------------------------

    interaction_time = (
        datetime.utcnow()
        - timedelta(
            days=random.randint(
                0,
                90
            ),
            hours=random.randint(
                0,
                23
            ),
            minutes=random.randint(
                0,
                59
            )
        )
    )

    # ----------------------------------------------
    # Create Interaction
    # ----------------------------------------------

    interaction = Interaction(

        user_id=user.id,

        content_id=content.id,

        clicked=clicked,

        liked=liked,

        saved=saved,

        shared=shared,

        watch_time=watch_time,

        read_time=read_time,

        scroll_depth=scroll_depth,

        interaction_time=interaction_time
    )

    db.add(interaction)

    existing_pairs.add(pair)

    created += 1

    # ----------------------------------------------
    # Progress
    # ----------------------------------------------

    if created % 100 == 0:

        print(
            f"Created {created} "
            f"/ {NUM_INTERACTIONS}"
        )


# ==================================================
# COMMIT
# ==================================================

db.commit()


# ==================================================
# RESULTS
# ==================================================

total_interactions = (
    db.query(Interaction)
    .count()
)

print()
print("======================================")
print("INTERACTION GENERATION COMPLETE")
print("======================================")

print(
    f"New interactions     : {created}"
)

print(
    f"Total interactions    : "
    f"{total_interactions}"
)

print("======================================")


db.close()