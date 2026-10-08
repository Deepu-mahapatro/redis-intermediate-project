# Redis Lists

## 1. Introduction

Redis Lists are an ordered collection of strings in Redis.

A Redis List allows elements to be added and removed from **both the left and right ends** of the list.

This makes Redis Lists useful for implementing data structures such as:

- Queues
- Stacks
- Task queues
- Job processing systems
- Activity streams

In this project, Redis Lists are used to implement a simple **Task Queue**.

---

## 2. Why Redis Lists?

A task queue needs to maintain the order in which tasks are added.

For example:

```text
Task A
Task B
Task C
```

If the queue follows **First In, First Out (FIFO)** behavior:

```text
Task A → Process first
Task B → Process second
Task C → Process third
```

Redis Lists provide operations from both ends, making this easy to implement.

For this project, we use:

```text
RPUSH → Add task
LPOP  → Process task
```

Therefore:

```text
RPUSH + LPOP = FIFO Queue
```

---

## 3. Redis List Structure

A Redis List can be visualized as:

```text
┌─────────┬─────────┬─────────┐
│ Task A  │ Task B  │ Task C  │
└─────────┴─────────┴─────────┘
    ↑                       ↑
   LEFT                    RIGHT
```

Redis allows operations from either end:

```text
LEFT  ← [ Task A | Task B | Task C ] → RIGHT
```

Examples:

```text
LPUSH → Add to left
RPUSH → Add to right

LPOP  → Remove from left
RPOP  → Remove from right
```

---

# 4. Redis List Commands

The following Redis List commands were practiced in this project:

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

---

## 5. RPUSH

### Purpose

`RPUSH` adds one or more elements to the **right side** of a Redis List.

### Syntax

```text
RPUSH key value [value ...]
```

### Example

```text
RPUSH task_queue "Task A"
```

Then:

```text
RPUSH task_queue "Task B"
```

Then:

```text
RPUSH task_queue "Task C"
```

The List becomes:

```text
Task A → Task B → Task C
```

### Important Point

`RPUSH` returns the new length of the List.

For example:

```text
RPUSH task_queue "Task A"
```

may return:

```text
1
```

After adding another task:

```text
RPUSH task_queue "Task B"
```

returns:

```text
2
```

---

# 6. LPUSH

### Purpose

`LPUSH` adds elements to the **left side** of a Redis List.

### Syntax

```text
LPUSH key value [value ...]
```

### Example

```text
LPUSH task_queue "Task A"
```

Then:

```text
LPUSH task_queue "Task B"
```

The List becomes:

```text
Task B → Task A
```

This happens because every new element is inserted at the left.

---

# 7. LPOP

### Purpose

`LPOP` removes and returns the element from the **left side** of the List.

### Syntax

```text
LPOP key
```

Example:

```text
LPOP task_queue
```

If the List contains:

```text
Task A
Task B
Task C
```

the result is:

```text
Task A
```

After the operation:

```text
Task B
Task C
```

---

# 8. RPOP

### Purpose

`RPOP` removes and returns the element from the **right side**.

### Syntax

```text
RPOP key
```

Example:

```text
RPOP task_queue
```

If the List contains:

```text
Task A
Task B
Task C
```

the result is:

```text
Task C
```

Remaining:

```text
Task A
Task B
```

---

# 9. LRANGE

### Purpose

`LRANGE` retrieves elements from a specific range of a List without removing them.

### Syntax

```text
LRANGE key start stop
```

To retrieve all elements:

```text
LRANGE task_queue 0 -1
```

Example output:

```text
1) "Task A"
2) "Task B"
3) "Task C"
```

### Important Point

Redis List indexes are zero-based:

```text
Task A → index 0
Task B → index 1
Task C → index 2
```

`-1` represents the last element.

Therefore:

```text
LRANGE task_queue 0 -1
```

means:

```text
Start from the first element
and continue until the last element.
```

---

# 10. LLEN

### Purpose

`LLEN` returns the number of elements in a List.

### Syntax

```text
LLEN key
```

Example:

```text
LLEN task_queue
```

If the queue contains:

```text
Task A
Task B
Task C
```

the result is:

```text
3
```

---

# 11. LREM

### Purpose

`LREM` removes elements from a List based on their value.

### Syntax

```text
LREM key count value
```

Example:

```text
LREM task_queue 1 "Task B"
```

This removes one occurrence of:

```text
Task B
```

from the List.

---

# 12. LTRIM

### Purpose

`LTRIM` keeps only a specified range of elements and removes the remaining elements.

### Syntax

```text
LTRIM key start stop
```

Example:

```text
LTRIM task_queue 0 1
```

If the List contains:

```text
Task A
Task B
Task C
Task D
```

after the command only:

```text
Task A
Task B
```

remain.

---

# 13. Manual Redis / Memurai Practice

The Redis List commands were first practiced manually using the Memurai CLI.

Example:

```text
RPUSH task_queue "Task A"
RPUSH task_queue "Task B"
RPUSH task_queue "Task C"
```

Then the queue was inspected:

```text
LRANGE task_queue 0 -1
```

Expected result:

```text
Task A
Task B
Task C
```

Queue size:

```text
LLEN task_queue
```

Expected:

```text
3
```

Then the first task was processed:

```text
LPOP task_queue
```

Expected:

```text
Task A
```

Remaining queue:

```text
Task B
Task C
```

This manual practice was completed before integrating the List into Django.

---

# 14. Practical Use Case — Task Queue

The project uses the Redis List as a simple **Task Queue**.

Redis key:

```text
task_queue
```

Example:

```text
Task A
Task B
Task C
```

The queue follows:

```text
First In
   ↓
First Out
```

Therefore:

```text
RPUSH → Add task at the end
LPOP  → Process task from the beginning
```

---

# 15. Task Queue Architecture

The implementation follows:

```text
                  Postman
                     │
                     │ POST /tasks/
                     ▼
                 Django View
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

---

# 16. Django Implementation

The Redis List key is defined as:

```python
TASK_QUEUE = "task_queue"
```

The Django application uses the shared Redis client:

```python
from config.redis_client import redis_client
```

---

## 17. Adding a Task

The API endpoint for adding a task is:

```text
POST /tasks/
```

Example request:

```json
{
    "task": "Send Email"
}
```

The Django view performs:

```python
position = redis_client.rpush(
    TASK_QUEUE,
    task
)
```

This executes the Redis operation:

```text
RPUSH task_queue "Send Email"
```

The returned value represents the new queue length.

The API response contains:

```json
{
    "message": "Task added successfully",
    "task": "Send Email",
    "queue_position": 1
}
```

---

# 18. Processing a Task

The API endpoint for processing a task is:

```text
POST /tasks/process/
```

The Django view performs:

```python
task = redis_client.lpop(TASK_QUEUE)
```

This executes:

```text
LPOP task_queue
```

If a task exists, it is removed from the left side and returned.

Example response:

```json
{
    "message": "Task processed successfully",
    "task": "Send Email"
}
```

---

# 19. Empty Queue Handling

The Django implementation also handles the case where no tasks are available.

If:

```python
redis_client.lpop(TASK_QUEUE)
```

returns:

```text
None
```

the API returns:

```json
{
    "message": "No tasks available"
}
```

with HTTP status:

```text
404
```

This prevents the application from trying to process a nonexistent task.

---

# 20. Postman Testing

### Add Task

Request:

```text
POST http://127.0.0.1:8000/tasks/
```

Body:

```json
{
    "task": "Task A"
}
```

Then add more tasks:

```json
{
    "task": "Task B"
}
```

```json
{
    "task": "Task C"
}
```

The Redis List becomes:

```text
Task A
Task B
Task C
```

---

## 21. Process Task

Request:

```text
POST http://127.0.0.1:8000/tasks/process/
```

The first response should contain:

```json
{
    "message": "Task processed successfully",
    "task": "Task A"
}
```

The next request processes:

```text
Task B
```

and then:

```text
Task C
```

This demonstrates FIFO behavior.

---

# 22. Redis Verification

After adding tasks through Postman, the Redis state can be inspected using:

```text
LRANGE task_queue 0 -1
```

Example:

```text
1) "Task A"
2) "Task B"
3) "Task C"
```

After processing the first task:

```text
LPOP task_queue
```

Redis returns:

```text
"Task A"
```

Checking again:

```text
LRANGE task_queue 0 -1
```

gives:

```text
1) "Task B"
2) "Task C"
```

This confirms that the Django API is actually modifying the Redis List.

---

# 23. Complete End-to-End Flow

### Adding a Task

```text
Postman
   │
   │ POST /tasks/
   ▼
Django
   │
   │ Read JSON body
   ▼
Extract task
   │
   ▼
redis_client.rpush()
   │
   ▼
RPUSH task_queue task
   │
   ▼
Redis List
   │
   ▼
New queue length
   │
   ▼
Django JSON Response
   │
   ▼
Postman
```

### Processing a Task

```text
Postman
   │
   │ POST /tasks/process/
   ▼
Django
   │
   ▼
redis_client.lpop()
   │
   ▼
LPOP task_queue
   │
   ▼
First task removed
   │
   ▼
Django JSON Response
   │
   ▼
Postman
```

---

# 24. FIFO Behavior

The most important concept demonstrated by this implementation is **FIFO — First In, First Out**.

Suppose tasks are added in this order:

```text
1. Task A
2. Task B
3. Task C
```

Redis stores:

```text
Task A → Task B → Task C
```

Processing happens using:

```text
LPOP
```

Therefore:

```text
Task A → First
Task B → Second
Task C → Third
```

The task that entered first is processed first.

---

# 25. List Commands Summary

| Command | Purpose |
|---|---|
| `LPUSH` | Add element to the left |
| `RPUSH` | Add element to the right |
| `LPOP` | Remove element from the left |
| `RPOP` | Remove element from the right |
| `LRANGE` | Read elements in a range |
| `LLEN` | Get List length |
| `LREM` | Remove elements by value |
| `LTRIM` | Keep only a specified range |

For the Task Queue implementation, the main commands are:

```text
RPUSH
LPOP
```

---

# 26. Key Learning

The most important idea from Redis Lists is:

```text
Redis List
    +
RPUSH
    +
LPOP
    ↓
FIFO Task Queue
```

Redis Lists are useful when **order matters** and elements need to be inserted or removed from either end.

In this project, the List was not studied only as a Redis command. It was converted into a practical Django feature — a **Task Queue** — and tested through both Postman and the Memurai CLI.

---

## 27. Implementation Status

Redis Lists are completely implemented in this project:

```text
Redis Lists                  ✅ 100%

LPUSH                        ✅
RPUSH                        ✅
LPOP                         ✅
RPOP                         ✅
LRANGE                       ✅
LLEN                         ✅
LREM                         ✅
LTRIM                        ✅

Task Queue                   ✅
Django Integration           ✅
Postman Testing              ✅
Redis Verification           ✅
End-to-End Flow              ✅
```
