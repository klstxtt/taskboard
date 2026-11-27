# TaskBoard

## Purpose

TaskBoard is a small task-management REST API built with FastAPI. Version 0.1 exposes
CRUD endpoints on tasks stored in memory. It is the base project of the ESIEE DevSecOps
course: later sessions add CI/CD, security scans and a database.

## Requirements

- Python 3.11 or newer (`python --version`)
- Git

## Installation

```bash
git clone <repo-url> taskboard
cd taskboard
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
- Health check: `GET /health` returns `{"status": "ok"}`

| Method | Path | Description | Success |
| --- | --- | --- | --- |
| POST | `/tasks` | Create a task | 201 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{task_id}` | Get one task | 200 |
| PATCH | `/tasks/{task_id}` | Update only the fields sent | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |

An unknown `task_id` returns 404.

## Tests

```bash
pytest
```

## Environment variables

Copy `.env.example` to `.env` and adapt the values for your machine:

```bash
cp .env.example .env
```

**Never commit `.env`**: it is ignored by `.gitignore`. Only `.env.example`, with
placeholder values, belongs in the repository.

| Variable | Purpose |
| --- | --- |
| `APP_ENV` | Environment name (`development`, `production`, ...) |
| `LOG_LEVEL` | Logging level |
| `DATABASE_URL` | Database connection string (used in a later session) |
| `SECRET_KEY` | Application secret (used in a later session) |

## Project structure

```
taskboard/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app and /health
│   ├── schemas.py         # Pydantic models
│   └── routers/
│       ├── __init__.py
│       └── tasks.py       # /tasks endpoints and in-memory store
├── tests/
│   ├── __init__.py
│   └── test_tasks.py
├── docs/
├── .gitignore
├── .env.example
├── README.md
└── requirements.txt
```
