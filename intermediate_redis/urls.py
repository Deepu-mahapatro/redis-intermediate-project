from django.urls import path

from .views import (
    add_task,
    process_task,
    interests,
    check_interest,
    count_interests,
    remove_interest,
    move_interest,
    union_interests,
    common_interests,
    different_interests,
    add_leaderboard_score,
    get_leaderboard,
    get_leaderboard_descending,
    get_member_score,
    get_member_rank,
    get_member_reverse_rank,
    remove_leaderboard_member,
    get_leaderboard_count,
    count_leaderboard_range,
    get_leaderboard_by_score

)


urlpatterns = [

    # ========================================================
    # Redis List — Task Queue
    # ========================================================

    path("tasks/", add_task),
    path("tasks/process/", process_task),


    # ========================================================
    # Redis Set — User Interests
    # ========================================================

    # POST → SADD
    # GET  → SMEMBERS
    path(
        "users/<int:user_id>/interests/",
        interests
    ),

    # GET → SISMEMBER
    path(
        "users/<int:user_id>/interests/check/",
        check_interest
    ),
    
    #GET -> SCARD
    path(
    "users/<int:user_id>/interests/count/",
    count_interests
    ),
    
    #DELETE -> SREM
    path(
    "users/<int:user_id>/interests/remove/",
    remove_interest
    ),
    
    #POST -> SMOVE 
    path(
    "users/<int:user_id>/interests/move/",
    move_interest
    ),
    
    #GET -> SUNION
    path(
    "users/<int:user_id>/interests/all/",
    union_interests
    ),
    
    #GET -> SINTER
    path(
    "users/<int:user_id>/interests/common/",
    common_interests
    ),
    
    #GET -> SDIFF
    path(
    "users/<int:user_id>/interests/different/",
    different_interests
    ),
    
    #SORTED SET  
    #POST —> ZADD
    path(
        "leaderboard/add/",
        add_leaderboard_score,
        name="add_leaderboard_score"),
    
    #GET -> ZRANGE
    path(
        "leaderboard/",
        get_leaderboard,
        name="get_leaderboard"
    ),
    
    #GET -> ZREVRANGE
    path(
    "leaderboard/top/",
    get_leaderboard_descending,
    name="get_leaderboard_descending"
    ),
    
    #GET -> ZSCORE
    path(
    "leaderboard/score/<str:member>/",
    get_member_score,
    name="get_member_score"
    ),
    
    #GET -> ZRANK
    path(
    "leaderboard/rank/<str:member>/",
    get_member_rank,
    name="get_member_rank"
    ),
    
    #GET -> ZREVRANK
    path(
    "leaderboard/reverse-rank/<str:member>/",
    get_member_reverse_rank,
    name="get_member_reverse_rank"
    ),
    
    #DELETE -> ZREM
    path(
    "leaderboard/remove/<str:member>/",
    remove_leaderboard_member,
    name="remove_leaderboard_member"
    ),
    
    #GET -> ZCARD
    path(
    "leaderboard/count/",
    get_leaderboard_count,
    name="get_leaderboard_count"
    ),
    
    #GET -> ZCOUNT
    path(
    "leaderboard/count-range/",
    count_leaderboard_range,
    name="count_leaderboard_range"
    ),
    
    #GET -> ZRANGEBYSCORE
    path(
    "leaderboard/by-score/",
    get_leaderboard_by_score,
    name="get_leaderboard_by_score"
    ),
    
    
]