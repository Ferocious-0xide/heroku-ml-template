# ML Heroku Template

Template for deploying machine learning models on Heroku with Redis queue and PostgreSQL support.

## Features
- CPU-only TensorFlow for Heroku compatibility
- Redis queue for async processing
- PostgreSQL for model storage and vector embeddings
- Separate worker dynos for ML inference
- RESTful API endpoints
- Status checking for async jobs

## Setup
1. Clone this repository
2. Add your ML model
3. Customize preprocessing in `app/ml/model.py`
4. Update requirements.txt if needed
5. Deploy to Heroku:
   ```
   heroku create
   heroku addons:create heroku-redis:hobby-dev
   heroku addons:create heroku-postgresql:standard-0
   heroku run alembic upgrade head
   git push heroku main
   heroku ps:scale worker=Standard-1x
   ```

## Database Features
- Model storage in PostgreSQL BLOB fields
- Vector embeddings support with pgvector
- Automatic migrations with Alembic

## Environment Variables
- REDIS_URL: Redis connection URL
- DATABASE_URL: PostgreSQL connection URL
- MAX_QUEUE_SIZE: Maximum queue size for predictions
