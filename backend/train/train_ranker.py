import os
import sys
import joblib
import numpy as np

from sklearn.ensemble import RandomForestRegressor


# ============================================================
# ADD BACKEND DIRECTORY TO PYTHON PATH
# ============================================================

BACKEND_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BACKEND_DIR)


# ============================================================
# LOAD APPLICATION DATABASE
# ============================================================

from app.database.connection import (
    SessionLocal,
    Base,
    engine
)


# ============================================================
# IMPORT ALL MODELS
# ============================================================

from app.models.user import User
from app.models.interaction import Interaction
from app.models.content import Content


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)

print("Database initialized successfully.")


# ============================================================
# DATABASE DEBUG INFORMATION
# ============================================================

print()
print("======================================")
print("DATABASE INFORMATION")
print("======================================")

print("DATABASE URL:")
print(engine.url)

connection = engine.connect()

print()
print("TABLES IN DATABASE:")
print(
    connection.dialect.get_table_names(connection)
)

print()
print("TABLES REGISTERED IN SQLALCHEMY:")
print(
    Base.metadata.tables.keys()
)

connection.close()


# ============================================================
# CREATE DATABASE SESSION
# ============================================================

db = SessionLocal()


# ============================================================
# BUILD TRAINING DATA
# ============================================================

print()
print("======================================")
print("BUILDING RANKING TRAINING DATA")
print("======================================")


interactions = (
    db.query(
        Interaction,
        Content
    )
    .join(
        Content,
        Interaction.content_id == Content.id
    )
    .all()
)


print(
    f"Interactions loaded : {len(interactions)}"
)


# ============================================================
# TRAINING ARRAYS
# ============================================================

X = []
y = []


# ============================================================
# CONVERT INTERACTIONS INTO TRAINING EXAMPLES
# ============================================================

for interaction, content in interactions:

    # --------------------------------------------------------
    # Engagement features
    # --------------------------------------------------------

    clicked = int(
        interaction.clicked or False
    )

    liked = int(
        interaction.liked or False
    )

    saved = int(
        interaction.saved or False
    )

    shared = int(
        interaction.shared or False
    )

    watch_time = float(
        interaction.watch_time or 0
    )

    read_time = float(
        interaction.read_time or 0
    )

    scroll_depth = float(
        interaction.scroll_depth or 0
    )


    # --------------------------------------------------------
    # Engagement score
    #
    # This becomes the target that the ranking model learns.
    # --------------------------------------------------------

    engagement_score = (
        1.0 * clicked
        + 2.0 * liked
        + 3.0 * saved
        + 4.0 * shared
        + 0.01 * watch_time
        + 0.01 * read_time
        + 2.0 * scroll_depth
    )


    # --------------------------------------------------------
    # Content features
    # --------------------------------------------------------

    title_length = len(
        content.title or ""
    )

    description_length = len(
        content.description or ""
    )


    # --------------------------------------------------------
    # Feature vector
    # --------------------------------------------------------

    features = [

        # User engagement
        clicked,
        liked,
        saved,
        shared,

        watch_time,
        read_time,
        scroll_depth,

        # Content characteristics
        title_length,
        description_length
    ]


    X.append(features)

    y.append(
        engagement_score
    )


# ============================================================
# CHECK TRAINING DATA
# ============================================================

print()
print("======================================")
print("TRAINING DATA")
print("======================================")

print(
    f"Training examples : {len(X)}"
)


if len(X) < 10:

    print()
    print("WARNING:")
    print(
        "Not enough interaction data to train "
        "a useful ranking model."
    )

    print()
    print(
        "Create more user interactions first."
    )

    print()

    db.close()

    raise SystemExit


# ============================================================
# CONVERT TO NUMPY ARRAYS
# ============================================================

X = np.array(
    X,
    dtype=np.float32
)

y = np.array(
    y,
    dtype=np.float32
)


# ============================================================
# TRAIN RANKING MODEL
# ============================================================

print()
print("======================================")
print("TRAINING RANKING MODEL")
print("======================================")


model = RandomForestRegressor(

    n_estimators=150,

    max_depth=10,

    random_state=42,

    n_jobs=-1
)


model.fit(
    X,
    y
)


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_DIR = "trained_models"

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


model_path = os.path.join(
    MODEL_DIR,
    "ranking_model.pkl"
)


joblib.dump(
    model,
    model_path
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

feature_names = [

    "clicked",
    "liked",
    "saved",
    "shared",

    "watch_time",
    "read_time",
    "scroll_depth",

    "title_length",
    "description_length"
]


print()
print("======================================")
print("FEATURE IMPORTANCE")
print("======================================")


for name, importance in zip(
    feature_names,
    model.feature_importances_
):

    print(
        f"{name:25s} : "
        f"{importance:.4f}"
    )


# ============================================================
# COMPLETE
# ============================================================

print()
print("======================================")
print("RANKING MODEL TRAINED SUCCESSFULLY")
print("======================================")

print(
    f"Training examples : {len(X)}"
)

print(
    f"Model saved       : {model_path}"
)

print("======================================")


# ============================================================
# CLOSE DATABASE
# ============================================================

db.close()

