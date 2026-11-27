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

## Validation rules

Invalid input is rejected with **422 Unprocessable Entity** (FastAPI's standard
validation response).

| Field | Rule |
| --- | --- |
| `title` | Required on create, trimmed, 1–200 characters, never `null` |
| `description` | Optional, at most 2,000 characters |
| `status` | One of `todo`, `in_progress`, `done`; default `todo`; never `null` |
| Unknown fields (e.g. `id`, `owner`) | Rejected, so a client cannot set server-side fields |
| `task_id` in the path | Positive integer (422 if not, 404 if unknown) |

`PATCH` only changes the fields that are sent.

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

## Security

Known risks and existing controls: [docs/security-notes.md](docs/security-notes.md).

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
│   ├── conftest.py        # fixtures: test client, empty store per test
│   └── test_tasks.py
├── docs/
│   └── security-notes.md  # first risk table (see below)
├── .gitignore
├── .env.example
├── README.md
└── requirements.txt
```
