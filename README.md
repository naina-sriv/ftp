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
| Authentication | JWT (python-jose) |
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
│   ├── main.py               # FastAPI app entry point
│   ├── models/               # SQLAlchemy ORM models ✅
│   │   ├── user.py
│   │   ├── issue.py
│   │   ├── constituency.py
│   │   └── vote.py
│   ├── schemas/              # Pydantic request/response schemas ✅
│   │   ├── user.py
│   │   ├── issue.py
│   │   └── vote.py
│   ├── api/                  # Route handlers (in progress)
│   │   ├── auth.py
│   │   ├── issues.py
│   │   └── votes.py
│   ├── core/                 # Config, JWT, security
│   ├── tasks/                # Celery task definitions
│   └── db/                   # Database session, init
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

> ✅ = implemented &nbsp;|&nbsp; remaining modules in active development

---

## Running Locally (once complete)

```bash
# Clone the repo
git clone https://github.com/naina-sriv/for-the-people.git
cd for-the-people

# Start all services
docker-compose up --build

# API will be available at
http://localhost:8000

# Interactive docs
http://localhost:8000/docs
```

---

## API Endpoints (planned)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login, receive JWT |
| GET | `/issues` | List issues in your constituency |
| POST | `/issues` | Report a new issue |
| POST | `/issues/{id}/vote` | Upvote an existing issue |
| GET | `/issues/{id}` | Get issue detail + status |

---

## Why I Built This

I kept watching real problems in communities go unacknowledged — not because no one cared, but because there was no structured way to make noise collectively. This project is an attempt to fix that with software: give people a way to validate each other's experiences and automatically surface what matters most to the most people.

---

## Status

> 🚧 Active development — schema and data models complete, API routes and async pipeline in progress.
