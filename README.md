# For The People ❤️

A civic tech platform for constituency‑level issue reporting, validation, and
prioritisation — because real problems deserve to be heard.

## What It Does

Citizens report issues in their constituency (infrastructure, utilities, public
safety, …). Issues are validated through a threshold‑based system: once enough
constituents up‑vote the same issue, it crosses an impact threshold and is
automatically escalated. The goal is simple — cut through noise and surface
the problems that matter to the most people.

## Current Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Client                           │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP
┌─────────────────────▼───────────────────────────────────┐
│                   FastAPI App                           │
│                                                         │
│  • JWT Authentication (constituency‑bound)              │
│  • Issue lifecycle management (REST APIs)               │
│  • Pydantic validation                                  │
│  • BackgroundTasks for async escalation checks          │
└──────────┬──────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│     PostgreSQL (or SQLite for local dev)                │
│                                                         │
│  • Issues, Users, Constituencies, Votes, Comments       │
└─────────────────────────────────────────────────────────┘
```

The escalation check runs inside a **FastAPI Background Task** — the API
responds instantly while vote‑counting and status updates happen
asynchronously.

## Tech Stack (actual implementation)

| Layer               | Technology               |
|---------------------|--------------------------|
| API Framework       | FastAPI                  |
| Authentication      | JWT (PyJWT + passlib)    |
| Database            | PostgreSQL (or SQLite)   |
| ORM / Validation    | SQLAlchemy + Pydantic v2  |
| Async Tasks         | FastAPI BackgroundTasks  |
| Testing             | pytest + httpx           |

> **Future improvements** (not yet implemented):  
> Celery + Redis for robust async task queue, Docker containerisation, CI/CD
> pipeline, real‑time notifications via WebSockets.

## Core Concepts

### Constituency‑Bound Access
Every user is tied to a constituency at registration. The JWT token carries
the constituency ID. All issue, comment, and vote endpoints automatically
scope data to the user’s own constituency — zero cross‑constituency noise.

### Threshold‑Based Validation
Issues start as `open`. Once **5 unique users** vote on an issue, a
background task sets `threshold_reached = true` and changes the status to
`escalated`. The threshold is configurable (currently hard‑coded to 5).

### Issue Lifecycle

```
 REPORTED (open)  →  VOTES ACCUMULATE  →  ESCALATED  →  (RESOLVED – future)
                          ↑
                  (threshold crossed)
```

## Project Structure

```
for-the-people/
├── app/
│   ├── core/
│   │   ├── config.py              # env vars + Pydantic Settings
│   │   ├── dependencies.py        # get_current_user dependency
│   │   └── security.py            # password hashing + JWT
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── constituency.py
│   │   ├── user.py
│   │   ├── issue.py
│   │   ├── comment.py
│   │   └── vote.py
│   ├── routers/                   # API route handlers
│   │   ├── auth.py                # register + login
│   │   ├── issue.py               # CRUD issues
│   │   ├── comments.py            # comments on an issue
│   │   └── votes.py               # voting + background escalation
│   ├── schema/                    # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── issue.py
│   │   ├── comment.py
│   │   ├── vote.py
│   │   ├── constituency.py
│   │   └── token.py
│   ├── db.py                      # DB session + Base
│   └── main.py                    # FastAPI app entry point
├── tests/
│   ├── conftest.py                # test fixtures (in‑memory SQLite)
│   └── test_routes.py             # full API test suite
├── .env                           # environment variables (not committed)
├── requirements.txt               # Python dependencies
└── README.md
```

## Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- PostgreSQL (optional — SQLite works out of the box for testing)

### Setup

```bash
git clone https://github.com/naina-sriv/for-the-people.git
cd for-the-people

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost/ftp  # or sqlite:///./app.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secret key:
```bash
openssl rand -hex 32
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method   | Endpoint                     | Description                                  | Auth |
|----------|------------------------------|----------------------------------------------|------|
| POST     | `/auth/register`             | Register a new user                          | No   |
| POST     | `/auth/login`                | Login, receive JWT                           | No   |
| GET      | `/issues`                    | List issues in your constituency             | Yes  |
| POST     | `/issues`                    | Report a new issue                           | Yes  |
| GET      | `/issues/{id}`               | Get issue detail                             | Yes  |
| PUT      | `/issues/{id}`               | Update your own issue                        | Yes  |
| DELETE   | `/issues/{id}`               | Delete your own issue                        | Yes  |
| POST     | `/issues/{id}/vote`          | Up‑vote an issue (one per user)              | Yes  |
| POST     | `/issues/{id}/comments`      | Add a comment to an issue                    | Yes  |
| GET      | `/issues/{id}/comments`      | List all comments for an issue               | Yes  |

## Testing

```bash
pytest tests/
```

The test suite uses an in‑memory SQLite database and covers:
- User registration & login (including duplicate email and bad password)
- Issue CRUD and constituency scoping
- Comment creation and listing
- Voting, duplicate prevention, and automatic threshold escalation

## Why I Built This

I kept watching real problems in communities go unacknowledged — not because
no one cared, but because there was no structured way to make noise
collectively. This project is an attempt to fix that with software: give
people a way to validate each other's experiences and automatically surface
what matters most.

## Future Roadmap

- Replace `BackgroundTasks` with **Celery + Redis** for reliable job queueing
- Add **Docker** and **docker‑compose** for one‑command development setup
- Real‑time notifications (WebSockets / SSE)
- Admin dashboard for constituency moderators
- ML‑based issue deduplication
```
