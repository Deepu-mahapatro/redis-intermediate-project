import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.redis_client import redis_client


# ============================================================
# REDIS LIST — TASK QUEUE
# ============================================================

TASK_QUEUE = "task_queue"


# ------------------------------------------------------------
# ADD TASK
# Redis Command: RPUSH
# ------------------------------------------------------------

@csrf_exempt
def add_task(request):

    # Only POST requests are allowed
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method is allowed"},
            status=405
        )

    try:
        # Convert JSON request body into Python dictionary
        data = json.loads(request.body)

        # Get task from request
        task = data.get("task")

        # Validate task
        if not task:
            return JsonResponse(
                {"error": "Task is required"},
                status=400
            )

        # Add task to the RIGHT side of Redis List
        # RPUSH → adds an element at the end
        position = redis_client.rpush(TASK_QUEUE, task)

        return JsonResponse(
            {
                "message": "Task added successfully",
                "task": task,
                "queue_position": position
            },
            status=201
        )

    except json.JSONDecodeError:

        # Invalid JSON
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )


# ------------------------------------------------------------
# PROCESS TASK
# Redis Command: LPOP
# ------------------------------------------------------------

@csrf_exempt
def process_task(request):

    # Only POST requests are allowed
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method is allowed"},
            status=405
        )

    # Remove the oldest task from the LEFT side
    # LPOP → removes the first element
    task = redis_client.lpop(TASK_QUEUE)

    # Queue is empty
    if task is None:
        return JsonResponse(
            {"message": "No tasks available"},
            status=404
        )

    return JsonResponse(
        {
            "message": "Task processed successfully",
            "task": task
        },
        status=200
    )


# ============================================================
# REDIS SET — USER INTERESTS
# ============================================================

# ------------------------------------------------------------
# USER INTERESTS
#
# POST → SADD     → Add an interest
# GET  → SMEMBERS → Get all interests
# ------------------------------------------------------------

@csrf_exempt
def interests(request, user_id):

    # Redis Set key for this user
    # Example:
    # user_id = 101
    # key = user:101:interests
    key = f"user:{user_id}:interests"


    # ========================================================
    # POST → ADD INTEREST
    # Redis Command: SADD
    # ========================================================

    if request.method == "POST":

        try:
            # Convert JSON request body into Python dictionary
            data = json.loads(request.body)

            # Get interest from request
            interest = data.get("interest")

            # Validate interest
            if not interest:
                return JsonResponse(
                    {"error": "Interest is required"},
                    status=400
                )

            # Add interest to Redis Set
            #
            # SADD returns:
            # 1 → new member added
            # 0 → member already exists
            added = redis_client.sadd(key, interest)

            # Interest already exists
            if added == 0:
                return JsonResponse(
                    {
                        "message": "Interest already exists",
                        "interest": interest
                    },
                    status=200
                )

            # Interest successfully added
            return JsonResponse(
                {
                    "message": "Interest added successfully",
                    "interest": interest
                },
                status=201
            )

        except json.JSONDecodeError:

            # Invalid JSON
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )


    # ========================================================
    # GET → GET ALL INTERESTS
    # Redis Command: SMEMBERS
    # ========================================================

    elif request.method == "GET":

        # Get all members from Redis Set
        interests = redis_client.smembers(key)

        return JsonResponse(
            {
                "user_id": user_id,

                # Convert Set to list
                # because JSON cannot directly serialize a Set
                "interests": list(interests)
            },
            status=200
        )


    # ========================================================
    # OTHER HTTP METHODS
    # ========================================================

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )
    
# ============================================================
# CHECK USER INTEREST
# Redis Command: SISMEMBER
# ============================================================

def check_interest(request, user_id):

    # Only GET requests are allowed
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get the interest from the URL query parameter
    #
    # Example:
    # /users/101/interests/check/?interest=Python
    interest = request.GET.get("interest")

    # Check whether interest was provided
    if not interest:
        return JsonResponse(
            {"error": "Interest query parameter is required"},
            status=400
        )

    # Redis Set key for this user
    # Example:
    # user:101:interests
    key = f"user:{user_id}:interests"

    # Check whether the interest exists in the Redis Set
    #
    # SISMEMBER returns:
    # 1 → member exists
    # 0 → member does not exist
    exists = redis_client.sismember(key, interest)

    return JsonResponse(
        {
            "user_id": user_id,
            "interest": interest,
            "exists": bool(exists)
        },
        status=200
    )
# ============================================================
# COUNT USER INTERESTS
# Redis Command: SCARD
# ============================================================

def count_interests(request, user_id):

    # Only GET requests are allowed
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Redis Set key for this user
    # Example:
    # user:101:interests
    key = f"user:{user_id}:interests"

    # Count the number of unique members
    # in the Redis Set
    count = redis_client.scard(key)

    return JsonResponse(
        {
            "user_id": user_id,
            "interest_count": count
        },
        status=200
    )
# ============================================================
# REMOVE USER INTEREST
# Redis Command: SREM
# ============================================================

@csrf_exempt
def remove_interest(request, user_id):

    # Only DELETE requests are allowed
    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Only DELETE method is allowed"},
            status=405
        )

    # Get interest from query parameter
    #
    # Example:
    # /users/101/interests/remove/?interest=AI
    interest = request.GET.get("interest")

    # Validate interest
    if not interest:
        return JsonResponse(
            {"error": "Interest query parameter is required"},
            status=400
        )

    # Redis Set key for this user
    key = f"user:{user_id}:interests"

    # Remove the interest from the Redis Set
    #
    # SREM returns:
    # 1 → member removed
    # 0 → member did not exist
    removed = redis_client.srem(key, interest)

    # Member was not present
    if removed == 0:
        return JsonResponse(
            {
                "message": "Interest does not exist",
                "interest": interest
            },
            status=404
        )

    # Member successfully removed
    return JsonResponse(
        {
            "message": "Interest removed successfully",
            "interest": interest
        },
        status=200
    )
# ============================================================
# MOVE INTEREST BETWEEN SETS
# Redis Command: SMOVE
# ============================================================

@csrf_exempt
def move_interest(request, user_id):

    # Only POST requests are allowed
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method is allowed"},
            status=405
        )

    # Get the interest from the query parameter
    #
    # Example:
    # /users/101/interests/move/?interest=AI
    interest = request.GET.get("interest")

    # Validate interest
    if not interest:
        return JsonResponse(
            {"error": "Interest query parameter is required"},
            status=400
        )

    # Source Set
    source_key = f"user:{user_id}:interests"

    # Destination Set
    destination_key = f"user:{user_id}:old_interests"

    # Move the member from source Set
    # to destination Set
    #
    # SMOVE returns:
    # 1 → member successfully moved
    # 0 → member does not exist in source Set
    moved = redis_client.smove(
        source_key,
        destination_key,
        interest
    )

    # Member was not found in source Set
    if moved == 0:
        return JsonResponse(
            {
                "message": "Interest does not exist in source set",
                "interest": interest
            },
            status=404
        )

    # Member successfully moved
    return JsonResponse(
        {
            "message": "Interest moved successfully",
            "interest": interest,
            "from": source_key,
            "to": destination_key
        },
        status=200
    )
# ============================================================
# UNION OF USER INTEREST SETS
# Redis Command: SUNION
# ============================================================

def union_interests(request, user_id):

    # Only GET requests are allowed
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # First Redis Set
    source_key = f"user:{user_id}:interests"

    # Second Redis Set
    destination_key = f"user:{user_id}:old_interests"

    # Get all unique members from both Sets
    #
    # SUNION combines both Sets.
    # Duplicate members appear only once.
    combined_interests = redis_client.sunion(
        source_key,
        destination_key
    )

    return JsonResponse(
        {
            "user_id": user_id,
            "interests": list(combined_interests)
        },
        status=200
    )
# ============================================================
# COMMON INTERESTS BETWEEN TWO USERS
# Redis Command: SINTER
# ============================================================

def common_interests(request, user_id):

    # Only GET requests are allowed
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get the second user's ID from the query parameter
    #
    # Example:
    # /users/101/interests/common/?other_user_id=102
    other_user_id = request.GET.get("other_user_id")

    # Validate the second user ID
    if not other_user_id:
        return JsonResponse(
            {"error": "other_user_id query parameter is required"},
            status=400
        )

    # Redis Set for the first user
    first_user_key = f"user:{user_id}:interests"

    # Redis Set for the second user
    second_user_key = f"user:{other_user_id}:interests"

    # Find common members between both Sets
    #
    # SINTER returns only members that exist
    # in BOTH Sets.
    common = redis_client.sinter(
        first_user_key,
        second_user_key
    )

    return JsonResponse(
        {
            "user_id": user_id,
            "other_user_id": int(other_user_id),
            "common_interests": list(common)
        },
        status=200
    )
# ============================================================
# DIFFERENT INTERESTS BETWEEN TWO USERS
# Redis Command: SDIFF
# ============================================================

def different_interests(request, user_id):

    # Only GET requests are allowed
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get the second user's ID from the query parameter
    #
    # Example:
    # /users/101/interests/different/?other_user_id=102
    other_user_id = request.GET.get("other_user_id")

    # Validate the second user ID
    if not other_user_id:
        return JsonResponse(
            {"error": "other_user_id query parameter is required"},
            status=400
        )

    # Redis Set for the first user
    first_user_key = f"user:{user_id}:interests"

    # Redis Set for the second user
    second_user_key = f"user:{other_user_id}:interests"

    # Find members that exist in the first Set
    # but NOT in the second Set
    #
    # SDIFF is directional:
    # first Set - second Set
    different = redis_client.sdiff(
        first_user_key,
        second_user_key
    )

    return JsonResponse(
        {
            "user_id": user_id,
            "other_user_id": int(other_user_id),
            "different_interests": list(different)
        },
        status=200
    )
    
# ============================================================
# REDIS SORTED SET — LEADERBOARD
# ============================================================

LEADERBOARD_KEY = "leaderboard"


@csrf_exempt
def add_leaderboard_score(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method is allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)

        member = data.get("member")
        score = data.get("score")

        # Validate required fields
        if not member:
            return JsonResponse(
                {"error": "Member is required"},
                status=400
            )

        if score is None:
            return JsonResponse(
                {"error": "Score is required"},
                status=400
            )

        # Add member and score to Redis Sorted Set
        result = redis_client.zadd(
            LEADERBOARD_KEY,
            {member: score}
        )

        return JsonResponse(
            {
                "message": "Leaderboard score added successfully",
                "member": member,
                "score": score,
                "new_member": result == 1
            },
            status=201
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except (ValueError, TypeError):
        return JsonResponse(
            {"error": "Score must be a valid number"},
            status=400
        )
# ============================================================
# REDIS SORTED SET — ZRANGE
# ============================================================

def get_leaderboard(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get all leaderboard members with their scores
    leaderboard = redis_client.zrange(
        LEADERBOARD_KEY,
        0,
        -1,
        withscores=True
    )

    # Convert Redis result into JSON-friendly format
    data = []

    for member, score in leaderboard:
        data.append(
            {
                "member": member,
                "score": score
            }
        )

    return JsonResponse(
        {
            "leaderboard": data
        },
        status=200
    )
# ============================================================
# REDIS SORTED SET — ZREVRANGE
# ============================================================

def get_leaderboard_descending(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get leaderboard members from highest score to lowest score
    leaderboard = redis_client.zrevrange(
        LEADERBOARD_KEY,
        0,
        -1,
        withscores=True
    )

    # Convert Redis result into JSON-friendly format
    data = []

    for member, score in leaderboard:
        data.append(
            {
                "member": member,
                "score": score
            }
        )

    return JsonResponse(
        {
            "leaderboard": data
        },
        status=200
    )
# ============================================================
# REDIS SORTED SET — ZSCORE
# ============================================================

def get_member_score(request, member):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get the score of the requested member
    score = redis_client.zscore(
        LEADERBOARD_KEY,
        member
    )

    # Member does not exist
    if score is None:
        return JsonResponse(
            {
                "error": "Member not found",
                "member": member
            },
            status=404
        )

    return JsonResponse(
        {
            "member": member,
            "score": score
        },
        status=200
    )
# ============================================================
# REDIS SORTED SET — ZRANK
# ============================================================

def get_member_rank(request, member):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get the ascending rank of the member
    rank = redis_client.zrank(
        LEADERBOARD_KEY,
        member
    )

    # Member does not exist
    if rank is None:
        return JsonResponse(
            {
                "error": "Member not found",
                "member": member
            },
            status=404
        )

    return JsonResponse(
        {
            "member": member,
            "rank": rank
        },
        status=200
    )
# ============================================================
# REDIS SORTED SET — ZREVRANK
# ============================================================

def get_member_reverse_rank(request, member):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    # Get the descending rank of the member
    rank = redis_client.zrevrank(
        LEADERBOARD_KEY,
        member
    )

    # Member does not exist
    if rank is None:
        return JsonResponse(
            {
                "error": "Member not found",
                "member": member
            },
            status=404
        )

    return JsonResponse(
        {
            "member": member,
            "rank": rank
        },
        status=200
    )
# ============================================================
# REDIS SORTED SET — ZREM
# ============================================================

@csrf_exempt
def remove_leaderboard_member(request, member):
    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Only DELETE method is allowed"},
            status=405
        )

    # Remove the member from the Sorted Set
    result = redis_client.zrem(
        LEADERBOARD_KEY,
        member
    )

    # Member does not exist
    if result == 0:
        return JsonResponse(
            {
                "error": "Member not found",
                "member": member
            },
            status=404
        )

    return JsonResponse(
        {
            "message": "Member removed successfully",
            "member": member
        },
        status=200
    )
# ============================================================
# REDIS SORTED SET — ZCARD
# ============================================================

def get_leaderboard_count(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    count = redis_client.zcard(LEADERBOARD_KEY)

    return JsonResponse(
        {
            "leaderboard_members": count
        },
        status=200
    )
# ============================================================
# REDIS SORTED SET — ZCOUNT
# ============================================================

def count_leaderboard_range(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    min_score = request.GET.get("min_score")
    max_score = request.GET.get("max_score")

    if min_score is None or max_score is None:
        return JsonResponse(
            {
                "error": "min_score and max_score are required"
            },
            status=400
        )

    try:
        min_score = float(min_score)
        max_score = float(max_score)

        count = redis_client.zcount(
            LEADERBOARD_KEY,
            min_score,
            max_score
        )

        return JsonResponse(
            {
                "min_score": min_score,
                "max_score": max_score,
                "count": count
            },
            status=200
        )

    except ValueError:
        return JsonResponse(
            {"error": "Scores must be valid numbers"},
            status=400
        )
# ============================================================
# REDIS SORTED SET — ZRANGEBYSCORE
# ============================================================

def get_leaderboard_by_score(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    min_score = request.GET.get("min_score")
    max_score = request.GET.get("max_score")

    if min_score is None or max_score is None:
        return JsonResponse(
            {
                "error": "min_score and max_score are required"
            },
            status=400
        )

    try:
        min_score = float(min_score)
        max_score = float(max_score)

        members = redis_client.zrangebyscore(
            LEADERBOARD_KEY,
            min_score,
            max_score,
            withscores=True
        )

        data = []

        for member, score in members:
            data.append(
                {
                    "member": member,
                    "score": score
                }
            )

        return JsonResponse(
            {
                "min_score": min_score,
                "max_score": max_score,
                "leaderboard": data
            },
            status=200
        )

    except ValueError:
        return JsonResponse(
            {"error": "Scores must be valid numbers"},
            status=400
        )