# ⚡ Redis Intermediate Project

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">

  <img src="https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">

  <img src="https://img.shields.io/badge/Redis-Data_Structures-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">

  <img src="https://img.shields.io/badge/Memurai-Windows-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Memurai">

  <img src="https://img.shields.io/badge/Postman-API_Testing-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman">

  <img src="https://img.shields.io/badge/Git-GitHub-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">

</p>

<p align="center">

  <b>A practical Redis project focused on Lists, Sets, Sorted Sets, and real-world Django integration.</b>

</p>

---

# 📌 About the Project

This project is a practical **Redis learning and implementation project** built with **Django and Redis/Memurai**.

The purpose of this project is to move beyond basic Redis caching and understand how Redis **data structures** can be used to solve real backend problems.

Instead of learning Redis commands only from theory, each data structure was:

```text
Concept
   ↓
Redis Command
   ↓
Manual Memurai CLI Practice
   ↓
Practical Use Case
   ↓
Django Integration
   ↓
Postman Testing
   ↓
Redis Verification
   ↓
End-to-End Understanding
```

The project currently focuses on three important Redis data structures:

```text
Redis Lists
     ↓
Task Queue

Redis Sets
     ↓
User Interests

Redis Sorted Sets
     ↓
Leaderboard
```

---

# 🎯 Project Objectives

The project was designed to understand Redis data structures practically.

### Primary Objectives

- Understand Redis Lists
- Understand Redis Sets
- Understand Redis Sorted Sets
- Practice Redis commands directly using Memurai CLI
- Integrate Redis with Django
- Build practical backend use cases
- Expose Redis operations through HTTP APIs
- Test APIs using Postman
- Verify Redis data directly through the CLI
- Understand how Redis commands map to backend functionality
- Understand when to choose Lists, Sets, or Sorted Sets
- Trace complete request and response flows

---

# 🏗️ Architecture

The project uses a simple architecture:

```text
                    ┌─────────────────────┐
                    │   Client / Postman  │
                    └──────────┬──────────┘
                               │
                               │ HTTP Request
                               ▼
                    ┌─────────────────────┐
                    │       Django        │
                    │    API / Views      │
                    └──────────┬──────────┘
                               │
                               │ Redis Commands
                               ▼
                    ┌─────────────────────┐
                    │    Redis Client     │
                    │      redis-py       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Redis / Memurai   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
           Lists             Sets        Sorted Sets
              │                │                │
              ▼                ▼                ▼
         Task Queue      User Interests     Leaderboard
```

### Core Principle

> **Django provides the application/API layer, while Redis provides specialized in-memory data structures for solving specific backend problems.**

Unlike Project 1, this project does **not** use Redis primarily as a caching layer.

The focus here is understanding Redis data structures and their practical backend applications.

---

# 🚀 Redis Data Structures Implemented

| Redis Data Structure | Practical Use Case |
|---|---|
| Lists | Task Queue |
| Sets | User Interests |
| Sorted Sets | Leaderboard |

---

# 📋 Redis Lists

Redis Lists are **ordered collections** that allow elements to be added and removed from both ends.

### Practical Use Case

A **Task Queue** was implemented using:

```text
RPUSH
   +
LPOP
   ↓
FIFO Queue
```

Example:

```text
Task A
Task B
Task C
```

Processing order:

```text
Task A
   ↓
Task B
   ↓
Task C
```

### Commands Practiced

```text
LPUSH
RPUSH
LPOP
RPOP
LRANGE
LLEN
LREM
LTRIM
```

### Main Learning

```text
Need ordered data?
        ↓
      Redis List
```

### Django APIs

```text
POST /tasks/
POST /tasks/process/
```

The complete implementation, Redis commands, Task Queue flow, Django integration, Postman testing, and Redis verification are documented in:

**[03-redis-lists.md](docs/03-redis-lists.md)**

---

# 🔵 Redis Sets

Redis Sets are **unordered collections of unique members**.

The same member cannot be stored twice.

### Practical Use Case

A **User Interests / Tags** system was implemented.

Example:

```text
user:101:interests

Python
Django
Redis
AI
```

Adding `Python` again does not create a duplicate.

### Commands Practiced

```text
SADD
SMEMBERS
SISMEMBER
SCARD
SREM
SMOVE
SUNION
SINTER
SDIFF
```

### Set Operations

```text
SADD
   ↓
Add Interest

SISMEMBER
   ↓
Check Interest

SCARD
   ↓
Count Interests

SREM
   ↓
Remove Interest

SMOVE
   ↓
Move Interest

SUNION
   ↓
Combine Sets

SINTER
   ↓
Find Common Interests

SDIFF
   ↓
Find Different Interests
```

### Django APIs

```text
POST   /users/<id>/interests/
GET    /users/<id>/interests/
GET    /users/<id>/interests/check/
GET    /users/<id>/interests/count/
DELETE /users/<id>/interests/remove/
POST   /users/<id>/interests/move/
GET    /users/<id>/interests/all/
GET    /users/<id>/interests/common/
GET    /users/<id>/interests/different/
```

### Main Learning

```text
Need unique data?
        ↓
      Redis Set
```

The complete implementation is documented in:

**[04-redis-sets.md](docs/04-redis-sets.md)**

---

# 🏆 Redis Sorted Sets

Redis Sorted Sets combine:

```text
Unique Member
      +
    Score
```

Redis maintains members according to their scores.

### Practical Use Case

A **Leaderboard System** was implemented.

Example:

```text
Deepu → 1000
Rahul → 850
Arjun → 700
Kiran → 600
```

### Commands Practiced

```text
ZADD
ZRANGE
ZREVRANGE
ZSCORE
ZRANK
ZREVRANK
ZREM
ZCARD
ZCOUNT
ZRANGEBYSCORE
```

### Main Operations

```text
ZADD
   ↓
Add / Update Score

ZRANGE
   ↓
Ascending Order

ZREVRANGE
   ↓
Descending Order

ZSCORE
   ↓
Get Member Score

ZRANK
   ↓
Ascending Rank

ZREVRANK
   ↓
Descending Rank

ZREM
   ↓
Remove Member

ZCARD
   ↓
Count Members

ZCOUNT
   ↓
Count Score Range

ZRANGEBYSCORE
   ↓
Get Members by Score Range
```

### Django APIs

```text
POST   /leaderboard/add/
GET    /leaderboard/
GET    /leaderboard/top/
GET    /leaderboard/score/<member>/
GET    /leaderboard/rank/<member>/
GET    /leaderboard/reverse-rank/<member>/
DELETE /leaderboard/remove/<member>/
GET    /leaderboard/count/
GET    /leaderboard/count-range/
GET    /leaderboard/by-score/
```

### Main Learning

```text
Need unique data
       +
Need scores / ordering / ranking
       ↓
Redis Sorted Set
```

The complete implementation is documented in:

**[05-redis-sorted-sets.md](docs/05-redis-sorted-sets.md)**

---

# 🧠 Redis Data Structure Decision

One of the main goals of this project is understanding **which Redis data structure should be selected for a particular problem**.

```text
                What does the problem need?
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
       Ordering       Uniqueness     Score + Rank
          │              │              │
          ▼              ▼              ▼
        LIST            SET        SORTED SET
          │              │              │
          ▼              ▼              ▼
      Task Queue    User Interests   Leaderboard
```

### Simple Decision Rule

```text
Need ordered collection?
        ↓
      LIST

Need unique members?
        ↓
       SET

Need unique members + scores + ranking?
        ↓
   SORTED SET
```

---

# 🔄 Complete Learning Flow

Every Redis data structure followed the same practical learning process:

```text
1. Understand the Concept
            ↓
2. Learn Redis Commands
            ↓
3. Practice Commands in Memurai CLI
            ↓
4. Select a Real Backend Use Case
            ↓
5. Implement in Django
            ↓
6. Create API Endpoint
            ↓
7. Test using Postman
            ↓
8. Inspect Redis Directly
            ↓
9. Understand Internal Flow
            ↓
10. Verify End-to-End Behavior
```

This approach makes the project focused on **understanding how Redis actually works inside a backend application**.

---

# 🌐 API Testing

Postman was used to test the Django APIs.

The general flow is:

```text
Postman
   ↓
HTTP Request
   ↓
Django View
   ↓
Redis Client
   ↓
Redis Command
   ↓
Redis Data Structure
   ↓
Django Response
   ↓
Postman
```

After API testing, Redis was directly inspected using Memurai CLI.

This provides two levels of verification:

```text
API Response
     +
Redis State
     ↓
Complete Understanding
```

---

# 🔍 Redis CLI / Memurai Practice

Redis commands were not learned only through Django.

They were manually executed using the Memurai CLI.

Examples:

### Lists

```text
RPUSH task_queue "Task A"
LRANGE task_queue 0 -1
LPOP task_queue
```

### Sets

```text
SADD user:101:interests Python
SMEMBERS user:101:interests
SISMEMBER user:101:interests Python
```

### Sorted Sets

```text
ZADD leaderboard 1000 Deepu
ZREVRANGE leaderboard 0 -1 WITHSCORES
ZSCORE leaderboard Deepu
```

This helped connect:

```text
Redis Command
      ↓
Redis Data Structure
      ↓
Django Method
      ↓
HTTP API
```

---

# 🧪 Testing Approach

The project was tested at multiple levels.

### 1. Redis CLI

Used to verify Redis commands and stored data.

### 2. Django

Redis connectivity and Redis operations were verified through the Django application.

### 3. Postman

HTTP APIs were tested with different request methods and inputs.

### 4. Redis Verification

After API operations, Redis was inspected again to verify the actual stored state.

---

# 📁 Project Structure

```text
redis-intermediate-project/
│
├── README.md
│
├── docs/
│   ├── 01-project-overview.md
│   ├── 02-architecture.md
│   ├── 03-redis-lists.md
│   ├── 04-redis-sets.md
│   └── 05-redis-sorted-sets.md
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── redis_client.py
│   ├── asgi.py
│   └── wsgi.py
│
├── intermediate_redis/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── manage.py
```

---

# 🛠️ Technology Stack

### Backend

- **Python**
- **Django**

### Redis

- **Redis**
- **Memurai** for Redis-compatible local development on Windows

### API Testing

- **Postman**

### Development Tools

- **VS Code**
- **Git**
- **GitHub**

---

# ⚙️ Setup

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd redis-intermediate-project
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
```

> `.env` should never be committed to GitHub.

The repository provides:

```text
.env.example
```

as a reference.

---

## 5. Run Migrations

```bash
python manage.py migrate
```

---

## 6. Start Redis / Memurai

Make sure the Redis-compatible Memurai service is running.

Verify using:

```bash
memurai-cli ping
```

Expected output:

```text
PONG
```

---

## 7. Start Django

```bash
python manage.py runserver
```

The Django application will then run on:

```text
http://127.0.0.1:8000/
```

---

# 📚 Documentation

The complete learning journey is divided into five focused documents.

| Document | Description |
|---|---|
| `01-project-overview.md` | Project purpose, objectives, scope, and completed topics |
| `02-architecture.md` | Complete Django + Redis architecture and request flows |
| `03-redis-lists.md` | Redis Lists and Task Queue implementation |
| `04-redis-sets.md` | Redis Sets and User Interests implementation |
| `05-redis-sorted-sets.md` | Redis Sorted Sets and Leaderboard implementation |

### Documentation Flow

```text
01 Project Overview
        ↓
02 Architecture
        ↓
03 Redis Lists
        ↓
04 Redis Sets
        ↓
05 Redis Sorted Sets
```

---

# 🎓 Learning Outcomes

After completing this stage of the project, the following concepts were practically understood:

### Redis Lists

- Ordered collections
- Adding elements from both ends
- Removing elements from both ends
- FIFO queue implementation
- `LPUSH`
- `RPUSH`
- `LPOP`
- `RPOP`
- `LRANGE`
- `LLEN`
- `LREM`
- `LTRIM`

### Redis Sets

- Unique members
- Unordered collections
- Membership checking
- Counting unique members
- Removing members
- Moving members between Sets
- Union
- Intersection
- Difference
- `SADD`
- `SMEMBERS`
- `SISMEMBER`
- `SCARD`
- `SREM`
- `SMOVE`
- `SUNION`
- `SINTER`
- `SDIFF`

### Redis Sorted Sets

- Unique members with scores
- Score-based ordering
- Leaderboards
- Member scores
- Member ranking
- Reverse ranking
- Score-range queries
- Counting score ranges
- `ZADD`
- `ZRANGE`
- `ZREVRANGE`
- `ZSCORE`
- `ZRANK`
- `ZREVRANK`
- `ZREM`
- `ZCARD`
- `ZCOUNT`
- `ZRANGEBYSCORE`

### Backend Integration

- Django + Redis integration
- Redis Python client
- HTTP API design
- JSON responses
- Postman testing
- Redis CLI verification
- End-to-end request tracing

---

# 📊 Project Status

```text
Redis Intermediate Project
│
├── Project Setup
│      ✅ Complete
│
├── Redis Lists
│      ✅ 100%
│      ├── LPUSH
│      ├── RPUSH
│      ├── LPOP
│      ├── RPOP
│      ├── LRANGE
│      ├── LLEN
│      ├── LREM
│      └── LTRIM
│
├── Redis Sets
│      ✅ 100%
│      ├── SADD
│      ├── SMEMBERS
│      ├── SISMEMBER
│      ├── SCARD
│      ├── SREM
│      ├── SMOVE
│      ├── SUNION
│      ├── SINTER
│      └── SDIFF
│
└── Redis Sorted Sets
       ✅ 100%
       ├── ZADD
       ├── ZRANGE
       ├── ZREVRANGE
       ├── ZSCORE
       ├── ZRANK
       ├── ZREVRANK
       ├── ZREM
       ├── ZCARD
       ├── ZCOUNT
       └── ZRANGEBYSCORE
```

---

# 🧠 Final Mental Model

The main lesson from this project is understanding **which Redis data structure solves which backend problem**.

```text
                         REDIS
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
           LIST           SET       SORTED SET
             │             │             │
             ▼             ▼             ▼
        Ordered Data   Unique Data   Score + Ranking
             │             │             │
             ▼             ▼             ▼
        Task Queue    User Interests  Leaderboard
```

The complete backend flow is:

```text
                         CLIENT
                           │
                           ▼
                         DJANGO
                           │
                           ▼
                     REDIS CLIENT
                           │
                           ▼
                    REDIS / MEMURAI
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
           LIST           SET       SORTED SET
             │             │             │
             ▼             ▼             ▼
        Task Queue    User Interests  Leaderboard
                           │
                           ▼
                         RESPONSE
```

---

# 🚀 Project Scope

This project intentionally focuses on three core Redis data structures:

```text
Redis Lists
Redis Sets
Redis Sorted Sets
```

Topics such as:

```text
Transactions
Pipelining
Pub/Sub
Streams
Lua Scripting
Persistence
Connection Pooling
Replication
Sentinel
ACL / Security
Redis Cluster
Sharding
Production Redis Architecture
```

are outside the scope of this current project and can be explored through subsequent Redis learning projects.

This keeps the project focused on developing a strong practical understanding of Redis data structures before moving into more advanced Redis architecture and distributed-system concepts.

---

# ⭐ Key Takeaway

> **The purpose of this project was not just to memorize Redis commands, but to understand which Redis data structure should be used for a particular backend problem, how the commands work, how they are integrated into Django, and how the complete request flows from an API client to Redis and back.**

```text
Need ordered data?
        ↓
      LIST
        ↓
   Task Queue

Need unique data?
        ↓
       SET
        ↓
 User Interests

Need unique data + score + ranking?
        ↓
   SORTED SET
        ↓
   Leaderboard
```

---

## 🔗 Related Documentation

- [Project Overview](docs/01-project-overview.md)
- [Architecture](docs/02-architecture.md)
- [Redis Lists](docs/03-redis-lists.md)
- [Redis Sets](docs/04-redis-sets.md)
- [Redis Sorted Sets](docs/05-redis-sorted-sets.md)
