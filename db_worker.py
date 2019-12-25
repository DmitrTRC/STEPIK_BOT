import redis
import json
import os
import fsm

REDIS_URL = os.environ.get('REDIS_URL')

ADMINS = [
    os.environ["STAFF_ID"]
]
state_db = {}


def get_current_state(user_id):
    if REDIS_URL:
        redis_db = redis.from_url(REDIS_URL)
        return redis_db.get(user_id)
    else:
        return state_db.get(user_id)


def set_state(user_id, value):
    if REDIS_URL:
        redis_db = redis.from_url(REDIS_URL)
        redis_db.set(user_id, value)
    else:
        state_db[user_id] = value
