import os

import joblib
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# ============================================================
# DATABASE
# ============================================================

from app.database.connection import SessionLocal
from app.models.content import Content


# ============================================================
# CONFIGURATION
# ============================================================

MAX_ARTICLES = 20000

MODEL_PATH = (
    "trained_models/"
    "productivity_model.pkl"
)


# ============================================================
# KEYWORD GROUPS
# ============================================================

PRODUCTIVE_KEYWORDS = [

    "learn",
    "tutorial",
    "guide",
    "how to",
    "research",
    "science",
    "scientific",
    "technology",
    "technology advances",
    "programming",
    "python",
    "machine learning",
    "artificial intelligence",
    "engineering",
    "education",
    "study",
    "analysis",
    "explained",
    "health",
    "medical",
    "climate",
    "environment",
    "finance",
    "financial",
    "investment",
    "economy",
    "business",
    "cybersecurity",
    "security",
    "space",
    "nasa",
    "energy",
    "renewable",
    "productivity",
    "career",
    "skills",
    "development"
]


NON_PRODUCTIVE_KEYWORDS = [

    "celebrity",
    "gossip",
    "viral",
    "meme",
    "reality show",
    "reality tv",
    "fashion",
    "party",
    "relationship",
    "dating",
    "influencer",
    "entertainment drama",
    "red carpet",
    "hollywood",
    "movie star",
    "actor spotted",
    "actress spotted",
    "social media feud",
    "controversy",
    "trending"
]


# ============================================================
# MANUAL SEED DATA
# ============================================================

seed_data = [

    # -------------------------------
    # PRODUCTIVE
    # -------------------------------

    (
        "Python programming tutorial for beginners",
        1
    ),

    (
        "How machine learning algorithms work",
        1
    ),

    (
        "NASA launches new satellite for climate research",
        1
    ),

    (
        "Understanding artificial intelligence and neural networks",
        1
    ),

    (
        "Guide to improving productivity and time management",
        1
    ),

    (
        "Learn SQL database queries and optimization",
        1
    ),

    (
        "New scientific research discovers potential treatment",
        1
    ),

    (
        "Technology advances in renewable energy",
        1
    ),

    (
        "How to build a web application using Python",
        1
    ),

    (
        "Financial education and investment strategies explained",
        1
    ),

    (
        "Cybersecurity best practices for protecting personal data",
        1
    ),

    (
        "Engineering students learn new programming techniques",
        1
    ),

    (
        "New study reveals important climate change findings",
        1
    ),

    (
        "Scientists discover new information about space",
        1
    ),

    (
        "How artificial intelligence is changing healthcare",
        1
    ),

    (
        "Investment strategies for long term financial planning",
        1
    ),

    # -------------------------------
    # NOT PRODUCTIVE
    # -------------------------------

    (
        "Celebrity shares latest vacation photos",
        0
    ),

    (
        "Famous actor spotted at a party",
        0
    ),

    (
        "Viral celebrity gossip spreads across social media",
        0
    ),

    (
        "Latest entertainment drama sparks online reactions",
        0
    ),

    (
        "Celebrity reveals details about personal life",
        0
    ),

    (
        "Viral video gets millions of views online",
        0
    ),

    (
        "Internet users react to hilarious viral video",
        0
    ),

    (
        "Latest celebrity fashion trend goes viral",
        0
    ),

    (
        "Reality television star causes controversy online",
        0
    ),

    (
        "Popular influencer shares a new social media post",
        0
    ),

    (
        "Trending meme takes over social media",
        0
    ),

    (
        "Celebrity relationship becomes latest internet controversy",
        0
    ),

    (
        "Hollywood actor attends celebrity party",
        0
    ),

    (
        "Celebrity feud becomes viral topic on social media",
        0
    )
]


# ============================================================
# BUILD WEAK LABEL FROM ARTICLE
# ============================================================

def weak_label_article(article):

    text = " ".join([
        article.title or "",
        article.description or "",
        article.content_text or ""
    ]).lower()

    category = (
        article.category or ""
    ).lower()

    productive_score = 0
    non_productive_score = 0

    # --------------------------------------------
    # Productive keywords
    # --------------------------------------------

    for keyword in PRODUCTIVE_KEYWORDS:

        if keyword in text:

            productive_score += 1

    # --------------------------------------------
    # Non-productive keywords
    # --------------------------------------------

    for keyword in NON_PRODUCTIVE_KEYWORDS:

        if keyword in text:

            non_productive_score += 1

    # --------------------------------------------
    # Category hints
    # --------------------------------------------

    productive_categories = [
        "technology",
        "science",
        "education",
        "health",
        "business",
        "finance",
        "environment"
    ]

    non_productive_categories = [
        "entertainment",
        "tv",
        "music",
        "celebrity",
        "gossip"
    ]

    if category in productive_categories:

        productive_score += 2

    if category in non_productive_categories:

        non_productive_score += 2

    # --------------------------------------------
    # Resolve label
    # --------------------------------------------

    if productive_score > non_productive_score:

        return 1

    if non_productive_score > productive_score:

        return 0

    # --------------------------------------------
    # Ambiguous article
    # --------------------------------------------

    return None


# ============================================================
# LOAD ARTICLES FROM DATABASE
# ============================================================

print("\nLoading articles from database...")

db = SessionLocal()

articles = (
    db.query(Content)
    .limit(MAX_ARTICLES)
    .all()
)

print(
    f"Articles loaded: {len(articles)}"
)


# ============================================================
# CREATE TRAINING DATA
# ============================================================

texts = []

labels = []

productive_count = 0
non_productive_count = 0
skipped_count = 0


for article in articles:

    label = weak_label_article(
        article
    )

    if label is None:

        skipped_count += 1

        continue

    text = " ".join([
        article.title or "",
        article.description or "",
        article.content_text or ""
    ])

    # Ignore extremely short articles

    if len(text.strip()) < 30:

        skipped_count += 1

        continue

    texts.append(text)

    labels.append(label)

    if label == 1:

        productive_count += 1

    else:

        non_productive_count += 1


# ============================================================
# ADD MANUAL SEED DATA
# ============================================================

for text, label in seed_data:

    texts.append(text)

    labels.append(label)

    if label == 1:

        productive_count += 1

    else:

        non_productive_count += 1


db.close()


# ============================================================
# CHECK DATA
# ============================================================

print("\nTraining dataset")
print("--------------------------------")

print(
    f"Total examples      : {len(texts)}"
)

print(
    f"Productive examples : {productive_count}"
)

print(
    f"Non-productive      : {non_productive_count}"
)

print(
    f"Skipped articles    : {skipped_count}"
)


if len(texts) < 100:

    raise RuntimeError(
        "Not enough training examples."
    )


# ============================================================
# TF-IDF + LOGISTIC REGRESSION
# ============================================================

model = Pipeline([

    (
        "tfidf",

        TfidfVectorizer(

            lowercase=True,

            stop_words="english",

            ngram_range=(1, 2),

            min_df=2,

            max_df=0.95,

            sublinear_tf=True
        )
    ),

    (
        "classifier",

        LogisticRegression(

            max_iter=2000,

            class_weight="balanced"
        )
    )
])


# ============================================================
# TRAIN
# ============================================================

print(
    "\nTraining productivity classifier..."
)

model.fit(
    texts,
    labels
)


# ============================================================
# SAVE MODEL
# ============================================================

os.makedirs(
    "trained_models",
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)


print("\n--------------------------------")
print("MODEL TRAINED SUCCESSFULLY")
print("--------------------------------")

print(
    f"Training examples : {len(texts)}"
)

print(
    f"Model saved       : {MODEL_PATH}"
)


# ============================================================
# TEST PREDICTIONS
# ============================================================

test_articles = [

    "NASA announces new space research mission",

    "Python programming tutorial for machine learning",

    "Scientists discover new renewable energy technology",

    "Celebrity shares controversial party photos",

    "Viral celebrity gossip spreads online",

    "Famous actor spotted at a party",

    "How to improve your productivity and time management",

    "New research reveals important information about climate change"
]


print("\nTEST PREDICTIONS")
print("--------------------------------")


for text in test_articles:

    probability = model.predict_proba(
        [text]
    )[0][1]

    print(
        f"{probability:.4f} | {text}"
    )