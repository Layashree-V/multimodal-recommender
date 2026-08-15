# FocusFeed content-type fix

This patch keeps the existing UI and adds real backend separation for:
- article
- blog
- video
- short

## API
`GET /content/feed?content_type=blog|video|short|article`
returns latest stored content for that type.

`GET /content/{content_id}` now returns content_type and media/source
metadata. Recommendation and search responses also include content_type.

## Ingestion
`backend/ingest.py` now ingests RSS news, blog RSS feeds, and YouTube RSS
videos. A record is stored as `short` only when the source explicitly
identifies it as a YouTube Short; normal YouTube videos remain `video`.

## Run
Keep your existing `.env` file in `backend/`.

From the backend directory:
    python ingest.py

Then start FastAPI normally.

If you add new content and want it to participate in personalized
recommendations, rebuild the FAISS content index using the project's
existing index-building command. Blogs/Videos/Shorts pages use
`/content/feed` and do not require FAISS.

## Frontend
Replace the current `App.jsx` with the supplied patched JSX file.
The existing visual design is preserved.
