# FastAPI Ingestion Service

A simple ingestion pipeline built with **FastAPI**, **Celery**, and **Redis**.  
It allows you to submit ingestion jobs, fetch data from external APIs, and store normalized entities in a database.

---

## 🚀 Features
- FastAPI REST endpoints for jobs and entities
- Celery workers for background ingestion tasks
- Redis as broker/backend
- SQLAlchemy ORM for persistence
- Modular routers for clean API structure
- Environment variables via `.env`

---

## 📦 Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/fastapi-ingestion-service.git
cd fastapi-ingestion-service


## 2. Create a virtual environment 

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows PowerShell

pip install -r requirements.txt

Create a .env file in the project root with your configuration:

REDIS_URL=redis://default:<password>@localhost:6379/0
DATABASE_URL=sqlite:///./test.db


Running the Service:
uvicorn app.main:app --reload or  python -m uvicorn app.main:app --reload

Start the Celery worker:
celery -A app.tasks worker --loglevel=info --pool=solo


Usage Examples
Submit a job:

curl -X POST "http://127.0.0.1:8000/jobs/ingest" \
     -H "Content-Type: application/json" \
     -d '{"providers":["api1","api2"]}'


Check job status:

curl http://127.0.0.1:8000/jobs/1


fastapi_ingestion_service/
│
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── tasks.py         # Celery tasks
│   ├── models.py        # SQLAlchemy models
│   ├── db.py            # Database session
│   └── routers/         # Modular routers (jobs, entities)
│
├── requirements.txt
├── .env.example
└── README.md

