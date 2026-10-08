# Redis Sorted Sets

## 1. Introduction

Redis Sorted Sets are a Redis data structure that combines:

```text
Unique Member
      +
    Score
```

Each member in a Sorted Set has a numerical score.

Redis automatically maintains the members according to their scores, which makes Sorted Sets especially useful for applications where data needs to be **ranked or ordered by a score**.

Common use cases include:

- Leaderboards
- Rankings
- Priority systems
- Score-based results
- Top-N queries
- Score-range queries

In this project, Redis Sorted Sets are used to implement a practical **Leaderboard System**.

---

# 2. Why Redis Sorted Sets?

A leaderboard needs to answer questions such as:

```text
Who has the highest score?
What is a player's score?
What is a player's rank?
Who are the top players?
How many players have scores between 700 and 900?
Which players are within a particular score range?
```

Redis Sorted Sets provide built-in commands for these operations.

Instead of manually sorting members in Django, Redis maintains the score-based ordering.

The basic model is:

```text id="a3pz9y"
Member → Score
```

Example:

```text id="q8a6j1"
Deepu → 1000
Rahul → 850
Arjun → 700
Kiran → 600
```

---

# 3. Redis Sorted Set Structure

The project's Sorted Set uses the Redis key:

```text id="h0z2gk"
leaderboard
```

Conceptually:

```text id="t3fq9h"
leaderboard

┌─────────┬────────┐
│ Member  │ Score  │
├─────────┼────────┤
│ Deepu   │ 1000   │
│ Rahul   │ 850    │
│ Arjun   │ 700    │
│ Kiran   │ 600    │
└─────────┴────────┘
```

Each member is unique.

For example:

```text id="z6m4pu"
ZADD leaderboard 1000 Deepu
```

adds `Deepu` with a score of `1000`.

If the same member is added again with another score:

```text id="sq8b6k"
ZADD leaderboard 1200 Deepu
```

Redis updates the score instead of creating a duplicate member.

---

# 4. Redis Sorted Set Commands

The following Sorted Set commands were practiced and implemented:

```text id="n0e8f1"
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

Each command provides a different leaderboard operation.

---

# 5. ZADD

## Purpose

`ZADD` adds a member with a score to a Sorted Set.

If the member already exists, its score is updated.

### Syntax

```text id="4zv6e7"
ZADD key score member [score member ...]
```

### Example

```text id="2xq8vf"
ZADD leaderboard 950 Deepu
ZADD leaderboard 850 Rahul
ZADD leaderboard 700 Arjun
ZADD leaderboard 600 Kiran
```

The Sorted Set now contains:

```text id="v8d2y1"
Deepu → 950
Rahul → 850
Arjun → 700
Kiran → 600
```

### Updating a Score

If:

```text id="2bgq3n"
ZADD leaderboard 1000 Deepu
```

is executed after Deepu already exists, Redis updates:

```text id="7v5p0c"
Deepu → 950
```

to:

```text id="e5c4w9"
Deepu → 1000
```

The member is not duplicated.

---

# 6. ZRANGE

## Purpose

`ZRANGE` retrieves members from a Sorted Set in **ascending score order**.

### Syntax

```text id="kv7qg9"
ZRANGE key start stop
```

To include scores:

```text id="6t7d4p"
ZRANGE key start stop WITHSCORES
```

Example:

```text id="2h4z9s"
ZRANGE leaderboard 0 -1 WITHSCORES
```

Possible result:

```text id="4u0e1f"
Kiran → 600
Arjun → 700
Rahul → 850
Deepu → 1000
```

The lowest score appears first.

---

# 7. ZREVRANGE

## Purpose

`ZREVRANGE` retrieves members in **descending score order**.

This is particularly useful for leaderboards.

### Syntax

```text id="2e0q9n"
ZREVRANGE key start stop
```

With scores:

```text id="x8u2pj"
ZREVRANGE key start stop WITHSCORES
```

Example:

```text id="4l3v9w"
ZREVRANGE leaderboard 0 -1 WITHSCORES
```

Result:

```text id="p7a1z3"
Deepu → 1000
Rahul → 850
Arjun → 700
Kiran → 600
```

The highest score appears first.

---

# 8. ZSCORE

## Purpose

`ZSCORE` retrieves the score of a specific member.

### Syntax

```text id="5p0q2v"
ZSCORE key member
```

Example:

```text id="9w7d4m"
ZSCORE leaderboard Deepu
```

Result:

```text id="7k2n8c"
1000
```

### Simple Meaning

```text id="b6f4x2"
ZSCORE
   ↓
"What is this member's score?"
```

---

# 9. ZRANK

## Purpose

`ZRANK` returns the rank of a member in **ascending score order**.

### Syntax

```text id="k5s8q2"
ZRANK key member
```

Example:

```text id="4v9h1z"
ZRANK leaderboard Deepu
```

If the Sorted Set is:

```text id="x7q3m8"
Kiran → 600
Arjun → 700
Rahul → 850
Deepu → 1000
```

then:

```text id="3n5c7a"
Deepu → rank 3
```

Redis ranks are **zero-based**.

Therefore:

```text id="7g2k9m"
Rank 0 → First
Rank 1 → Second
Rank 2 → Third
Rank 3 → Fourth
```

---

# 10. ZREVRANK

## Purpose

`ZREVRANK` returns the rank of a member in **descending score order**.

### Syntax

```text id="w6p3d1"
ZREVRANK key member
```

Example:

```text id="4x9n2b"
ZREVRANK leaderboard Deepu
```

With:

```text id="1a8v5c"
Deepu → 1000
Rahul → 850
Arjun → 700
Kiran → 600
```

Deepu has:

```text id="8y3f0q"
rank = 0
```

Rahul has:

```text id="2m7k4d"
rank = 1
```

This is the ranking model most useful for a leaderboard.

---

# 11. ZREM

## Purpose

`ZREM` removes a member from a Sorted Set.

### Syntax

```text id="q4n8y2"
ZREM key member [member ...]
```

Example:

```text id="j7p3s6"
ZREM leaderboard Kiran
```

The member `Kiran` is removed from the leaderboard.

---

# 12. ZCARD

## Purpose

`ZCARD` returns the total number of members in a Sorted Set.

### Syntax

```text id="n5x8c1"
ZCARD key
```

Example:

```text id="m2k7v9"
ZCARD leaderboard
```

If the leaderboard contains:

```text id="b4p6q0"
Deepu
Rahul
Arjun
Kiran
```

the result is:

```text id="y8s3d5"
4
```

---

# 13. ZCOUNT

## Purpose

`ZCOUNT` counts the number of members whose scores fall within a specified score range.

### Syntax

```text id="r6k1p8"
ZCOUNT key min max
```

Example:

```text id="u2v7m4"
ZCOUNT leaderboard 700 900
```

If the leaderboard contains:

```text id="5s8q3n"
Deepu → 1000
Rahul → 850
Arjun → 700
Kiran → 600
```

the members between `700` and `900` are:

```text id="g4x9d2"
Rahul
Arjun
```

Therefore:

```text id="f7m2k5"
2
```

---

# 14. ZRANGEBYSCORE

## Purpose

`ZRANGEBYSCORE` retrieves members whose scores fall within a specified range.

### Syntax

```text id="p3w8n6"
ZRANGEBYSCORE key min max
```

With scores:

```text id="k9d4s1"
ZRANGEBYSCORE key min max WITHSCORES
```

Example:

```text id="v6q2m8"
ZRANGEBYSCORE leaderboard 700 900 WITHSCORES
```

Result:

```text id="c5y1r7"
Arjun → 700
Rahul → 850
```

This is useful when an application needs to retrieve players within a particular score range.

---

# 15. Manual Redis / Memurai Practice

The Sorted Set commands were first practiced manually using the Memurai CLI.

The leaderboard was created using:

```text id="n2x7v5"
ZADD leaderboard 950 Deepu
ZADD leaderboard 850 Rahul
ZADD leaderboard 700 Arjun
ZADD leaderboard 600 Kiran
```

The leaderboard was inspected using:

```text id="s4p9m2"
ZRANGE leaderboard 0 -1 WITHSCORES
```

For highest-to-lowest ordering:

```text id="h7c3q8"
ZREVRANGE leaderboard 0 -1 WITHSCORES
```

A specific score was checked:

```text id="b1v6x9"
ZSCORE leaderboard Deepu
```

Ranks were checked using:

```text id="m8q2d5"
ZRANK leaderboard Deepu
ZREVRANK leaderboard Deepu
```

A member was removed using:

```text id="z3f7k1"
ZREM leaderboard Kiran
```

The total number of members was checked using:

```text id="q6n4y8"
ZCARD leaderboard
```

A score range was counted using:

```text id="t2m9p4"
ZCOUNT leaderboard 700 900
```

Members within a score range were retrieved using:

```text id="w5k1s7"
ZRANGEBYSCORE leaderboard 700 900 WITHSCORES
```

This manual practice was completed before and alongside the Django implementation.

---

# 16. Practical Use Case — Leaderboard

The project uses the Sorted Set to implement a simple leaderboard.

Redis key:

```text id="e8q3m6"
leaderboard
```

Example:

```text id="x
