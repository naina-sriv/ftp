# For The People 🗳️

A civic tech platform for constituency-level issue reporting, validation, and prioritization — because real problems deserve to be heard.

## What It Does

Citizens can report issues affecting their constituency (infrastructure, utilities, public safety, etc.). Issues are validated through a threshold-based system: once enough constituents report or upvote the same problem, it crosses an impact threshold and triggers automated escalation actions via an async pipeline.

The goal is simple — cut through noise and surface the issues that actually matter to the most people.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Client                           │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP
┌─────────────────────▼───────────────────────────────────┐
│                   FastAPI App                           │
│                                                         │
│  • JWT Authentication (constituency-bound)              │
│  • Issue lifecycle management (REST APIs)               │
│  • Pydantic validation                                  │
│  • Threshold evaluation logic                           │
└──────────┬──────────────────────┬───────────────────────┘
           │                      │
┌──────────▼──────────┐  ┌───────▼───────────────────────┐
│     PostgreSQL      │  │         Redis                  │
│                     │  │                                │
│  • Issues           │  │  • Celery broker               │
│  • Users            │  │  • Task queue                  │
│  • Constituencies   │  │  • Result backend              │
│  • Votes/Reports    │  └───────┬───────────────────────┘
└─────────────────────┘          │
                        ┌────────▼───────────────────────┐
                        │       Celery Worker             │
                        │                                 │
                        │  • Triggered when issue crosses │
                        │    impact threshold             │
                        │  • Escalation actions           │
                        │  • Notification dispatch        │
                        └────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Authentication | JWT (PyJWT) |
| Database | PostgreSQL |
| ORM / Validation | SQLAlchemy + Pydantic |
| Async Task Queue | Celery |
| Message Broker | Redis |
| Containerization | Docker + Docker Compose |

---

## Core Concepts

### Constituency-Bound Access
Every user is tied to a constituency at registration. JWT tokens encode constituency membership — users can only report, view, and vote on issues within their own constituency. This prevents cross-constituency noise and keeps data meaningful at a local level.

### Threshold-Based Validation
Issues don't get escalated just because one person reports them. A configurable threshold determines when an issue has enough validated reports to be considered high-impact. Once crossed, a Celery task is dispatched asynchronously to handle escalation — keeping the API response fast and the side effects decoupled.

### Issue Lifecycle
```
REPORTED → VALIDATED → ESCALATED → RESOLVED
              ↑
     (threshold crossed)
```

---

## Project Structure

```
for-the-people/
├── app/
│   ├── core/
│   │   ├── config.py              # Environment variables + settings ✅
│   │   ├── dependencies.py        # get_current_user dependency ✅
│   │   └── security.py            # Password hashing + JWT ✅
│   ├── models/                    # SQLAlchemy ORM models ✅
│   │   ├── __init__.py
│   │   ├── constituency.py
│   │   ├── user.py
│   │   ├── issue.py
│   │   ├── comment.py
│   │   └── vote.py
│   ├── routers/                   # Route handlers
│   │   ├── __init__.py
│   │   ├── auth.py                # Register + Login ✅
│   │   ├── issue.py               # Issue CRUD 🚧
│   │   ├── comments.py            # Comment routes 🚧
│   │   └── votes.py               # Voting + threshold logic 🚧
│   ├── schema/                    # Pydantic request/response schemas ✅
│   │   ├── user.py
│   │   ├── issue.py
│   │   ├── comment.py
│   │   ├── vote.py
│   │   ├── constituency.py
│   │   └── token.py
│   ├── tasks/                     # Celery task definitions
│   │   └── threshold.py           # Escalation trigger 🚧
│   ├── __init__.py
│   ├── db.py                      # Database session + Base ✅
│   └── main.py                    # FastAPI app entry point ✅
├── .env                           # Environment variables (not committed)
├── .gitignore                     ✅
├── docker-compose.yml             🚧
├── Dockerfile                     🚧
├── requirements.txt               ✅
└── README.md
```

> ✅ = implemented &nbsp;|&nbsp; 🚧 = in progress

---

## Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://user:password@localhost/ftp
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure secret key:
```bash
openssl rand -hex 32
```

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/naina-sriv/for-the-people.git
cd for-the-people

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your .env file (see above)

# Run the development server
uvicorn app.main:app --reload

# API available at
http://localhost:8000

# Interactive docs
http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description | Status |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | ✅ |
| POST | `/auth/login` | Login, receive JWT | ✅ |
| GET | `/issues` | List issues in your constituency | 🚧 |
| POST | `/issues` | Report a new issue | 🚧 |
| GET | `/issues/{id}` | Get issue detail + status | 🚧 |
| POST | `/issues/{id}/vote` | Vote on an issue | 🚧 |
| POST | `/issues/{id}/comments` | Comment on an issue | 🚧 |
| GET | `/issues/{id}/comments` | Get comments on an issue | 🚧 |

---

## Requirements

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic-settings
python-dotenv
PyJWT
passlib[bcrypt]
celery
redis
```

---

## Why I Built This

I kept watching real problems in communities go unacknowledged — not because no one cared, but because there was no structured way to make noise collectively. This project is an attempt to fix that with software: give people a way to validate each other's experiences and automatically surface what matters most to the most people.

---

## Status

> 🚧 Active development — models, schemas, and auth complete. Issue, comment, and vote routes plus async Celery pipeline in progress.