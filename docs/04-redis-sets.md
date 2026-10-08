# Redis Sets

## 1. Introduction

Redis Sets are an unordered collection of **unique members**.

The two most important properties of a Redis Set are:

```text
Unique
  +
Unordered
```

If the same member is added multiple times, Redis stores it only once.

In this project, Redis Sets are used to implement a practical **User Interests / Tags** system.

For example:

```text
user:101:interests
```

can contain:

```text
Python
Django
Redis
AI
```

If `Python` is added again, Redis does not create a duplicate.

---

## 2. Why Redis Sets?

Sets are useful when the application needs to store a collection where:

- Duplicate values should not exist.
- Membership needs to be checked.
- The number of unique members needs to be counted.
- Members need to be added or removed.
- Two collections need to be compared.
- Common or different members need to be identified.

This makes Redis Sets useful for:

- User interests
- Tags
- Unique visitors
- Permissions
- Roles
- Followers/following
- Membership tracking

In this project, the selected use case is:

```text
User Interests / Tags
```

---

# 3. Redis Set Structure

A Redis Set can be visualized as:

```text
user:101:interests

┌─────────┐
│ Python  │
├─────────┤
│ Django  │
├─────────┤
│ Redis   │
├─────────┤
│ AI      │
└─────────┘
```

Unlike a Redis List, the Set does not maintain an application-defined order.

The main property is uniqueness.

---

# 4. Redis Set Commands

The following Redis Set commands were practiced and implemented:

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

Each command solves a different Set operation.

---

# 5. SADD

## Purpose

`SADD` adds one or more members to a Set.

If the member already exists, Redis does not add a duplicate.

### Syntax

```text
SADD key member [member ...]
```

### Example

```text
SADD user:101:interests Python Django Redis AI
```

The Set becomes:

```text
Python
Django
Redis
AI
```

If we execute:

```text
SADD user:101:interests Python
```

again, `Python` is not duplicated.

### Important Point

This is one of the main differences between a Redis List and a Redis Set:

```text
List → Duplicate values are allowed
Set  → Duplicate values are not allowed
```

---

# 6. SMEMBERS

## Purpose

`SMEMBERS` returns all members of a Set.

### Syntax

```text
SMEMBERS key
```

Example:

```text
SMEMBERS user:101:interests
```

Possible output:

```text
1) "Python"
2) "Django"
3) "Redis"
4) "AI"
```

The order should not be treated as meaningful because Redis Sets are unordered.

---

# 7. SISMEMBER

## Purpose

`SISMEMBER` checks whether a specific member exists inside a Set.

### Syntax

```text
SISMEMBER key member
```

Example:

```text
SISMEMBER user:101:interests Python
```

If `Python` exists, Redis returns:

```text
1
```

If it does not exist:

```text
0
```

### Simple Meaning

```text
SISMEMBER
     ↓
"Does this member exist?"
```

---

# 8. SCARD

## Purpose

`SCARD` returns the number of unique members in a Set.

### Syntax

```text
SCARD key
```

Example:

```text
SCARD user:101:interests
```

If the Set contains:

```text
Python
Django
Redis
AI
```

the result is:

```text
4
```

Because Redis Sets contain unique values, `SCARD` counts unique members.

---

# 9. SREM

## Purpose

`SREM` removes one or more members from a Set.

### Syntax

```text
SREM key member [member ...]
```

Example:

```text
SREM user:101:interests AI
```

Before:

```text
Python
Django
Redis
AI
```

After:

```text
Python
Django
Redis
```

---

# 10. SMOVE

## Purpose

`SMOVE` moves a member from one Set to another Set.

### Syntax

```text
SMOVE source destination member
```

Example:

```text
SMOVE user:101:interests user:101:old_interests AI
```

The member:

```text
AI
```

is removed from:

```text
user:101:interests
```

and added to:

```text
user:101:old_interests
```

This is useful when an item needs to move between two groups.

---

# 11. SUNION

## Purpose

`SUNION` returns the combined members from two or more Sets.

### Syntax

```text
SUNION key [key ...]
```

Example:

```text
SUNION group:python group:ai
```

Suppose:

```text
group:python

Python
Django
Redis
```

and:

```text
group:ai

Python
AI
ML
```

The union contains:

```text
Python
Django
Redis
AI
ML
```

Duplicate members are automatically removed.

### Simple Meaning

```text
SUNION
   ↓
Everything from both Sets
```

---

# 12. SINTER

## Purpose

`SINTER` returns members that are common to two or more Sets.

### Syntax

```text
SINTER key [key ...]
```

Example:

```text
SINTER group:python group:ai
```

Given:

```text
group:python

Python
Django
Redis
```

and:

```text
group:ai

Python
AI
ML
```

the result is:

```text
Python
```

### Simple Meaning

```text
SINTER
   ↓
What exists in both Sets?
```

---

# 13. SDIFF

## Purpose

`SDIFF` returns members that exist in the first Set but do not exist in the following Sets.

### Syntax

```text
SDIFF key [key ...]
```

Example:

```text
SDIFF group:python group:ai
```

Given:

```text
group:python

Python
Django
Redis
```

and:

```text
group:ai

Python
AI
ML
```

the result is:

```text
Django
Redis
```

### Simple Meaning

```text
SDIFF
   ↓
What is in Set A but NOT in Set B?
```

---

# 14. Manual Redis / Memurai Practice

The Set commands were first practiced manually using the Memurai CLI.

Example:

```text
SADD user:101:interests Python Django Redis AI
```

Then the Set was inspected:

```text
SMEMBERS user:101:interests
```

Membership was checked:

```text
SISMEMBER user:101:interests Python
```

Count was checked:

```text
SCARD user:101:interests
```

A member was removed:

```text
SREM user:101:interests AI
```

Different Sets were then created to practice:

```text
SMOVE
SUNION
SINTER
SDIFF
```

This manual practice helped verify the Redis behavior before integrating the operations into Django.

---

# 15. Practical Use Case — User Interests

The project uses Redis Sets to store user interests.

The key format is:

```text
user:<user_id>:interests
```

Example:

```text
user:101:interests
```

Possible members:

```text
Python
Django
Redis
AI
```

Another user can have:

```text
user:102:interests
```

with:

```text
Python
Redis
ML
```

This allows the project to demonstrate both individual Set operations and Set comparison operations.

---

# 16. Django Integration

The Django application uses the shared Redis client:

```python
from config.redis_client import redis_client
```

For a user, the Redis key is generated dynamically:

```python
key = f"user:{user_id}:interests"
```

Therefore:

```text
user_id = 101
```

creates:

```text
user:101:interests
```

This gives every user a separate Redis Set.

---

# 17. Adding and Getting Interests

The main endpoint is:

```text
/users/<user_id>/interests/
```

### POST

A `POST` request adds an interest.

Example:

```text
POST /users/101/interests/
```

Request body:

```json
{
    "interest": "Python"
}
```

Django executes:

```python
redis_client.sadd(
    key,
    interest
)
```

This corresponds to:

```text
SADD user:101:interests Python
```

### GET

A `GET` request retrieves all interests.

```text
GET /users/101/interests/
```

Django executes:

```python
redis_client.smembers(key)
```

This corresponds to:

```text
SMEMBERS user:101:interests
```

Example response:

```json
{
    "user_id": "101",
    "interests": [
        "Python",
        "Redis",
        "AI",
        "Django"
    ]
}
```

---

# 18. Checking an Interest

The project provides an endpoint to check whether a user has a particular interest.

```text
GET /users/<user_id>/interests/check/?interest=Python
```

Example:

```text
GET /users/101/interests/check/?interest=Python
```

Django executes:

```python
redis_client.sismember(
    key,
    interest
)
```

This corresponds to:

```text
SISMEMBER user:101:interests Python
```

The result tells the application whether the interest exists.

---

# 19. Counting Interests

The project provides:

```text
GET /users/<user_id>/interests/count/
```

Example:

```text
GET /users/101/interests/count/
```

Django executes:

```python
redis_client.scard(key)
```

This corresponds to:

```text
SCARD user:101:interests
```

Example response:

```json
{
    "user_id": "101",
    "interest_count": 4
}
```

---

# 20. Removing an Interest

The project provides:

```text
DELETE /users/<user_id>/interests/remove/?interest=AI
```

Example:

```text
DELETE /users/101/interests/remove/?interest=AI
```

Django executes:

```python
redis_client.srem(
    key,
    interest
)
```

This corresponds to:

```text
SREM user:101:interests AI
```

If the member exists, it is removed from the Set.

---

# 21. Moving an Interest

The project also implements `SMOVE`.

Endpoint:

```text
POST /users/<user_id>/interests/move/?interest=AI
```

Example:

```text
POST /users/101/interests/move/?interest=AI
```

The operation moves the interest from:

```text
user:101:interests
```

to:

```text
user:101:old_interests
```

Django executes:

```python
redis_client.smove(
    source_key,
    destination_key,
    interest
)
```

This corresponds to:

```text
SMOVE user:101:interests user:101:old_interests AI
```

---

# 22. Union of Interests

The project provides an endpoint to combine the current and old interests:

```text
GET /users/<user_id>/interests/all/
```

Example:

```text
GET /users/101/interests/all/
```

Django uses:

```python
redis_client.sunion(
    current_key,
    old_key
)
```

This corresponds to:

```text
SUNION user:101:interests user:101:old_interests
```

The result contains all unique members from both Sets.

---

# 23. Common Interests

The project can find interests shared by two users.

Endpoint:

```text
GET /users/<user_id>/interests/common/?other_user_id=<other_id>
```

Example:

```text
GET /users/101/interests/common/?other_user_id=102
```

Django uses:

```python
redis_client.sinter(
    current_key,
    other_key
)
```

This corresponds to:

```text
SINTER user:101:interests user:102:interests
```

Example:

```text
User 101:
Python
Django
Redis
AI

User 102:
Python
Redis
ML
```

Common interests:

```text
Python
Redis
```

---

# 24. Different Interests

The project can also find interests that belong to one user but not another.

Endpoint:

```text
GET /users/<user_id>/interests/different/?other_user_id=<other_id>
```

Example:

```text
GET /users/101/interests/different/?other_user_id=102
```

Django uses:

```python
redis_client.sdiff(
    current_key,
    other_key
)
```

This corresponds to:

```text
SDIFF user:101:interests user:102:interests
```

Using:

```text
User 101:
Python
Django
Redis
AI
```

and:

```text
User 102:
Python
Redis
ML
```

the difference is:

```text
Django
AI
```

---

# 25. API-to-Redis Command Mapping

| Feature | HTTP API | Redis Command |
|---|---|---|
| Add Interest | `POST /users/<id>/interests/` | `SADD` |
| Get Interests | `GET /users/<id>/interests/` | `SMEMBERS` |
| Check Interest | `GET /users/<id>/interests/check/` | `SISMEMBER` |
| Count Interests | `GET /users/<id>/interests/count/` | `SCARD` |
| Remove Interest | `DELETE /users/<id>/interests/remove/` | `SREM` |
| Move Interest | `POST /users/<id>/interests/move/` | `SMOVE` |
| All Interests | `GET /users/<id>/interests/all/` | `SUNION` |
| Common Interests | `GET /users/<id>/interests/common/` | `SINTER` |
| Different Interests | `GET /users/<id>/interests/different/` | `SDIFF` |

---

# 26. Postman Testing Flow

The APIs were tested using Postman.

### Step 1 — Add Interests

```text
POST /users/101/interests/
```

Body:

```json
{
    "interest": "Python"
}
```

Repeat for:

```text
Django
Redis
AI
```

---

### Step 2 — Retrieve Interests

```text
GET /users/101/interests/
```

Example result:

```json
{
    "user_id": "101",
    "interests": [
        "Python",
        "Redis",
        "AI",
        "Django"
    ]
}
```

---

### Step 3 — Check Membership

```text
GET /users/101/interests/check/?interest=Python
```

This checks whether `Python` exists.

---

### Step 4 — Count Members

```text
GET /users/101/interests/count/
```

This returns the number of unique interests.

---

### Step 5 — Remove an Interest

```text
DELETE /users/101/interests/remove/?interest=AI
```

This removes `AI`.

---

### Step 6 — Move an Interest

```text
POST /users/101/interests/move/?interest=AI
```

This moves `AI` to:

```text
user:101:old_interests
```

---

### Step 7 — Compare Sets

Create another user:

```text
user:102:interests
```

Then use:

```text
GET /users/101/interests/common/?other_user_id=102
```

and:

```text
GET /users/101/interests/different/?other_user_id=102
```

This demonstrates `SINTER` and `SDIFF`.

---

# 27. Redis Verification

After using Postman, the Redis data can be inspected directly.

For example:

```text
SMEMBERS user:101:interests
```

This verifies the actual Set stored in Redis.

To inspect the old interests:

```text
SMEMBERS user:101:old_interests
```

For two users:

```text
SMEMBERS user:101:interests
SMEMBERS user:102:interests
```

The results can then be compared using:

```text
SINTER user:101:interests user:102:interests
```

or:

```text
SDIFF user:101:interests user:102:interests
```

This confirms that the Django API operations are directly reflected in Redis.

---

# 28. Complete Add-Interest Flow

```text
Postman
   │
   │ POST /users/101/interests/
   ▼
Django
   │
   │ Read JSON
   ▼
Extract interest
   │
   ▼
redis_client.sadd()
   │
   ▼
SADD user:101:interests Python
   │
   ▼
Redis Set
   │
   ▼
Redis result
   │
   ▼
Django JSON Response
   │
   ▼
Postman
```

---

# 29. Complete Common-Interest Flow

```text
Postman
   │
   │ GET /users/101/interests/common/?other_user_id=102
   ▼
Django
   │
   ▼
Build two Redis keys
   │
   ├── user:101:interests
   └── user:102:interests
   │
   ▼
redis_client.sinter()
   │
   ▼
SINTER
   │
   ▼
Redis calculates common members
   │
   ▼
Django receives result
   │
   ▼
JSON Response
   │
   ▼
Postman
```

---

# 30. Why Sets Were Selected for This Use Case

User interests are a good example for Redis Sets because duplicate interests should not exist.

For example, if a user adds:

```text
Python
Python
Python
```

the application should still represent:

```text
Python
```

only once.

Sets also make operations such as:

```text
Is this interest present?
How many unique interests exist?
What interests do two users share?
What interests are different?
```

simple Redis operations.

---

# 31. List vs Set

The project now contains both Redis Lists and Sets.

| Feature | Redis List | Redis Set |
|---|---|---|
| Ordering | Ordered | Unordered |
| Duplicates | Allowed | Not allowed |
| Main Use Case | Task Queue | User Interests |
| Add | `LPUSH` / `RPUSH` | `SADD` |
| Remove | `LPOP` / `RPOP` | `SREM` |
| Membership | Not the main purpose | `SISMEMBER` |
| Comparison | Not designed for it | `SUNION`, `SINTER`, `SDIFF` |

The important decision is:

```text
Need order?
    ↓
List

Need uniqueness?
    ↓
Set
```

---

# 32. Key Learning

The most important idea from Redis Sets is:

```text
Redis Set
    ↓
Unique Members
    ↓
Fast Membership Operations
    ↓
Set Comparison
```

The project demonstrates how Redis Sets can move beyond simple storage and provide built-in operations for:

```text
Add
Check
Count
Remove
Move
Union
Intersection
Difference
```

These operations were integrated into Django and tested through Postman and the Memurai CLI.

---

# 33. Implementation Status

Redis Sets are completely implemented in this project:

```text
Redis Sets                    ✅ 100%

SADD                          ✅
SMEMBERS                      ✅
SISMEMBER                     ✅
SCARD                         ✅
SREM                          ✅
SMOVE                         ✅
SUNION                        ✅
SINTER                        ✅
SDIFF                         ✅

User Interests Use Case       ✅
Django Integration            ✅
Postman Testing               ✅
Redis Verification            ✅
End-to-End Flow               ✅
```

The next Redis data structure documented in this project is **Sorted Sets**, implemented as a **Leaderboard System**.
