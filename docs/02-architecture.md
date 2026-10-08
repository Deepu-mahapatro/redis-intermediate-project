# Redis Intermediate Project

## 1. Architecture Overview

This project uses a simple architecture where **Django acts as the backend/API layer** and **Redis/Memurai acts as the data structure and in-memory data store**.

The project does not use Redis as a cache for this stage.

Instead, Redis is directly used to store and operate on:

- Lists
- Sets
- Sorted Sets

The overall architecture is:

```text
                  Client / Postman
                         │
                         │ HTTP Request
                         ▼
                  ┌──────────────┐
                  │    Django    │
                  │  API / Views │
                  └──────┬───────┘
                         │
                         │ Redis Commands
                         ▼
                  ┌──────────────┐
                  │ Redis Client │
                  │   redis-py   │
                  └──────┬───────┘
                         │
                         │ TCP
                         ▼
                  ┌──────────────┐
                  │ Redis /      │
                  │   Memurai    │
                  └──────┬───────┘
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
          Lists        Sets     Sorted Sets
```

---

## 2. Main Components

The project contains four main components:

```text
1. Client / Postman
2. Django Application
3. Redis Python Client
4. Redis / Memurai Server
```

Each component has a specific responsibility.

---

## 3. Client / Postman

Postman is used as the client for testing the APIs.

It sends HTTP requests to the Django application.

For example:

```text
POST /tasks/
```

or:

```text
GET /leaderboard/
```

Postman allows us to verify:

- HTTP methods
- Request data
- API responses
- Status codes
- Redis-backed operations

The client does not directly communicate with Redis.

The request always goes through Django.

```text
Postman
   ↓
Django
   ↓
Redis
```

---

## 4. Django Application

Django is the main backend application.

It receives HTTP requests and determines which Redis operation needs to be performed.

The Django application contains the Redis-related logic inside:

```text
intermediate_redis/
```

The main API logic is implemented in:

```text
intermediate_redis/views.py
```

The views handle operations for:

```text
Redis Lists
Redis Sets
Redis Sorted Sets
```

For example:

```python
redis_client.rpush(...)
```

is used for adding tasks to a Redis List.

Similarly:

```python
redis_client.sadd(...)
```

is used for adding members to a Redis Set.

And:

```python
redis_client.zadd(...)
```

is used for adding members and scores to a Redis Sorted Set.

---

## 5. Redis Client

The Django application communicates with Redis through the Python Redis client.

The connection is configured in:

```text
config/redis_client.py
```

The Redis client is created using:

```python
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
```

### Meaning

```text
host="localhost"
```

means Redis is running on the same computer as the Django application.

```text
port=6379
```

is the default Redis port.

```text
decode_responses=True
```

allows Redis responses to be returned as normal Python strings instead of byte strings.

---

## 6. Redis / Memurai

Redis is the actual data store used by the project.

On Windows, the project uses **Memurai**, which is Redis-compatible.

The application communicates with Memurai through the Redis protocol.

The same Redis data can therefore be inspected in two ways:

```text
Django Application
       ↓
Redis Client
       ↓
Redis / Memurai
```

and manually:

```text
Memurai CLI
       ↓
Redis / Memurai
```

This makes it possible to compare what the API does with what is actually stored in Redis.

---

# 7. Redis Data Structure Architecture

The project currently uses three Redis data structures.

```text
                    Redis / Memurai
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
        Lists             Sets        Sorted Sets
          │                │                │
          ▼                ▼                ▼
      Task Queue      User Interests     Leaderboard
```

Each structure solves a different problem.

---

## 8. List Architecture — Task Queue

Redis Lists are used to implement a simple task queue.

The Redis key is:

```text
task_queue
```

The flow is:

```text
Postman
   │
   │ POST /tasks/
   ▼
Django
   │
   │ RPUSH
   ▼
Redis List
task_queue
   │
   │ LPOP
   ▼
Processed Task
```

### Adding a Task

When a task is added:

```python
redis_client.rpush(
    "task_queue",
    task
)
```

The task is inserted at the right side of the List.

Example:

```text
Task A
Task B
Task C
```

### Processing a Task

When a task is processed:

```python
redis_client.lpop(
    "task_queue"
)
```

The first task is removed from the left side.

Therefore:

```text
RPUSH → Add at right
LPOP  → Remove from left
```

This produces:

```text
FIFO
First In → First Out
```

---

## 9. Set Architecture — User Interests

Redis Sets are used to store unique user interests.

The key format is:

```text
user:<user_id>:interests
```

Example:

```text
user:101:interests
```

The flow is:

```text
Postman
   │
   │ POST /users/101/interests/
   ▼
Django
   │
   │ SADD
   ▼
Redis Set
user:101:interests
```

Example Set:

```text
Python
Django
Redis
AI
```

Because Redis Sets store unique members, adding:

```text
Python
```

again does not create a duplicate.

---

## 10. Set Operations Architecture

The project also uses Redis Set operations to compare collections.

For example:

```text
User 101
   │
   ▼
user:101:interests

User 102
   │
   ▼
user:102:interests
```

These sets can be compared using:

```text
SUNION
SINTER
SDIFF
```

### Union

```text
SUNION
```

combines members from both sets.

```text
Set A + Set B
```

### Intersection

```text
SINTER
```

finds members common to both sets.

```text
Set A ∩ Set B
```

### Difference

```text
SDIFF
```

finds members that exist in the first set but not in the second.

```text
Set A - Set B
```

The Django application performs these operations through the Redis client.

---

# 11. Sorted Set Architecture — Leaderboard

Redis Sorted Sets are used to implement the project leaderboard.

The Redis key is:

```text
leaderboard
```

Each member has a score.

Example:

```text
Deepu → 1000
Rahul → 850
Arjun → 700
Kiran → 600
```

The architecture is:

```text
Postman
   │
   │ POST /leaderboard/add/
   ▼
Django
   │
   │ ZADD
   ▼
Redis Sorted Set
leaderboard
   │
   ├── Member
   └── Score
```

Redis automatically maintains the ordering based on scores.

---

## 12. Leaderboard Read Flow

To retrieve the leaderboard in ascending order:

```text
GET /leaderboard/
        ↓
Django
        ↓
ZRANGE
        ↓
Redis Sorted Set
        ↓
Ascending Results
```

To retrieve the leaderboard in descending order:

```text
GET /leaderboard/top/
        ↓
Django
        ↓
ZREVRANGE
        ↓
Redis Sorted Set
        ↓
Descending Results
```

---

## 13. Member Score Flow

To retrieve a specific member's score:

```text
GET /leaderboard/score/<member>/
        ↓
Django
        ↓
ZSCORE
        ↓
Redis
        ↓
Member Score
        ↓
JSON Response
```

Example:

```text
GET /leaderboard/score/Deepu/
```

Redis operation:

```text
ZSCORE leaderboard Deepu
```

---

## 14. Member Ranking Flow

The project supports both ascending and descending ranking.

### Ascending Rank

```text
GET /leaderboard/rank/<member>/
        ↓
Django
        ↓
ZRANK
        ↓
Redis
        ↓
Rank
```

### Descending Rank

```text
GET /leaderboard/reverse-rank/<member>/
        ↓
Django
        ↓
ZREVRANK
        ↓
Redis
        ↓
Rank
```

The ranks returned by Redis are **zero-based**.

For example:

```text
Rank 0 → First position
Rank 1 → Second position
Rank 2 → Third position
```

---

# 15. Score Range Architecture

The project also supports operations based on score ranges.

### Count members in a score range

```text
GET /leaderboard/count-range/
        ↓
Django
        ↓
ZCOUNT
        ↓
Redis
        ↓
Number of members
```

Example:

```text
min_score = 700
max_score = 900
```

### Retrieve members in a score range

```text
GET /leaderboard/by-score/
        ↓
Django
        ↓
ZRANGEBYSCORE
        ↓
Redis
        ↓
Matching members
        ↓
JSON Response
```

---

# 16. Complete Request Flow

The general request flow throughout the project is:

```text
                    Client / Postman
                           │
                           │ HTTP Request
                           ▼
                    Django URL Router
                           │
                           ▼
                    Django View
                           │
                           ▼
                    Redis Client
                           │
                           ▼
                  Redis Command
                           │
                           ▼
                   Redis / Memurai
                           │
                           ▼
                  Redis Data Structure
                           │
                           ▼
                    Redis Response
                           │
                           ▼
                    Django View
                           │
                           ▼
                    JSON Response
                           │
                           ▼
                       Postman
```

---

# 17. Example End-to-End Flow

Consider adding a new leaderboard member.

### Request

```http
POST /leaderboard/add/
```

Request body:

```json
{
    "member": "Deepu",
    "score": 1000
}
```

### Internal Flow

```text
1. Postman sends HTTP POST request
                ↓
2. Django receives the request
                ↓
3. Django reads member and score
                ↓
4. Django calls redis_client.zadd()
                ↓
5. Redis executes ZADD
                ↓
6. Member and score are stored
                ↓
7. Redis returns the operation result
                ↓
8. Django creates JSON response
                ↓
9. Postman displays the response
```

### Redis State

After the operation:

```text
leaderboard

Deepu → 1000
```

The same data can be verified manually using:

```text
ZRANGE leaderboard 0 -1 WITHSCORES
```

This confirms that the API operation actually modified Redis.

---

# 18. API-to-Redis Mapping

The project maps HTTP APIs to Redis commands.

| Feature | HTTP API | Redis Command |
|---|---|---|
| Add Task | `POST /tasks/` | `RPUSH` |
| Process Task | `POST /tasks/process/` | `LPOP` |
| Add Interest | `POST /users/<id>/interests/` | `SADD` |
| Get Interests | `GET /users/<id>/interests/` | `SMEMBERS` |
| Check Interest | `GET /users/<id>/interests/check/` | `SISMEMBER` |
| Count Interests | `GET /users/<id>/interests/count/` | `SCARD` |
| Remove Interest | `DELETE /users/<id>/interests/remove/` | `SREM` |
| Move Interest | `POST /users/<id>/interests/move/` | `SMOVE` |
| Union Interests | `GET /users/<id>/interests/all/` | `SUNION` |
| Common Interests | `GET /users/<id>/interests/common/` | `SINTER` |
| Different Interests | `GET /users/<id>/interests/different/` | `SDIFF` |
| Add Score | `POST /leaderboard/add/` | `ZADD` |
| Get Leaderboard | `GET /leaderboard/` | `ZRANGE` |
| Get Top Leaderboard | `GET /leaderboard/top/` | `ZREVRANGE` |
| Get Score | `GET /leaderboard/score/<member>/` | `ZSCORE` |
| Get Rank | `GET /leaderboard/rank/<member>/` | `ZRANK` |
| Get Reverse Rank | `GET /leaderboard/reverse-rank/<member>/` | `ZREVRANK` |
| Remove Member | `DELETE /leaderboard/remove/<member>/` | `ZREM` |
| Count Members | `GET /leaderboard/count/` | `ZCARD` |
| Count Score Range | `GET /leaderboard/count-range/` | `ZCOUNT` |
| Get Score Range | `GET /leaderboard/by-score/` | `ZRANGEBYSCORE` |

---

# 19. Redis Verification

One important part of this project is that API testing is followed by direct Redis verification.

For example:

```text
Postman
   ↓
POST /leaderboard/add/
   ↓
Django
   ↓
ZADD
   ↓
Redis
```

Then Redis can be checked directly:

```text
ZRANGE leaderboard 0 -1 WITHSCORES
```

This provides confirmation that the Django API and Redis data are connected correctly.

The same approach is used for:

- Lists
- Sets
- Sorted Sets

---

# 20. Project Architecture Summary

The architecture can be summarized as:

```text
                         ┌─────────────────┐
                         │   Postman /     │
                         │     Client      │
                         └────────┬────────┘
                                  │
                              HTTP Request
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Django      │
                         │   API / Views   │
                         └────────┬────────┘
                                  │
                             Redis Client
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Redis / Memurai │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
        ┌──────────┐        ┌──────────┐       ┌──────────────┐
        │  Lists   │        │   Sets   │       │ Sorted Sets  │
        └────┬─────┘        └────┬─────┘       └──────┬───────┘
             │                   │                    │
             ▼                   ▼                    ▼
         Task Queue        User Interests         Leaderboard
```

The key idea of this architecture is:

> **Django provides the application/API layer, while Redis provides specialized in-memory data structures for solving specific backend problems.**

This project therefore focuses on understanding not only Redis commands, but also **how those commands become useful application features through Django**.
