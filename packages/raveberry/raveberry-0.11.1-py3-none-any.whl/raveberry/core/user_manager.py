"""This module manages and counts user accesses and handles permissions."""
import time
from functools import wraps
from typing import Callable

import ipware
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from core import redis

# kick users after some time without any request
from core.lights import leds
from core.settings import storage

INACTIVITY_PERIOD = 600


def has_controls(user) -> bool:
    """Determines whether the given user is allowed to control playback."""
    return user.username == "mod" or is_admin(user)


def is_admin(user) -> bool:
    """Determines whether the given user is the admin."""
    return user.is_superuser


def update_user_count() -> None:
    """Go through all recent requests and delete those that were too long ago."""
    now = time.time()
    last_requests = redis.get("last_requests")
    for key, value in list(last_requests.items()):
        if now - value >= INACTIVITY_PERIOD:
            del last_requests[key]
            redis.put("last_requests", last_requests)
    redis.put("last_user_count_update", now)


def get_count() -> int:
    """Returns the number of currently active users.
    Updates this number after an intervals since the last update."""
    if time.time() - redis.get("last_user_count_update") >= 60:
        update_user_count()
    return len(redis.get("last_requests"))


def partymode_enabled() -> bool:
    """Determines whether partymode is enabled,
    based on the number of currently active users."""
    return len(redis.get("last_requests")) >= storage.get("people_to_party")


def get_client_ip(request: WSGIRequest):
    """Returns the origin IP of a given request or "" if not possible."""
    request_ip, _ = ipware.get_client_ip(request)
    if request_ip is None:
        request_ip = ""
    return request_ip


def try_vote(request_ip: str, queue_key: int, amount: int) -> bool:
    """If the user can not vote any more for the song into the given direction, return False.
    Otherwise, perform the vote and returns True."""
    # Votes are stored as individual (who, what) tuples in redis.
    # A mapping who -> [what, ...] is not used,
    # because each modification would require deserialization and subsequent serialization.
    # Without such a mapping we cannot easily find all votes belonging to a session key,
    # which would be required to update the view of a user whose client-votes got desynced.
    # This should never happen during normal usage, so we optimize for our main use case:
    # looking up whether a single user voted for a single song, which is constant with tuples.
    entry = str((request_ip, queue_key))
    allowed = True

    # redis transaction: https://github.com/Redis/redis-py#pipelines
    def check_entry(pipe) -> None:
        nonlocal allowed
        vote = pipe.get(entry)
        if vote is None:
            new_vote = amount
        else:
            new_vote = int(vote) + amount
        if new_vote < -1 or new_vote > 1:
            allowed = False
            return
        allowed = True
        # expire these entries to avoid accumulation over long runtimes.
        pipe.multi()
        pipe.set(entry, new_vote, ex=24 * 60 * 60)

    redis.connection.transaction(check_entry, entry)
    return allowed


def tracked(
    func: Callable[[WSGIRequest], HttpResponse]
) -> Callable[[WSGIRequest], HttpResponse]:
    """A decorator that stores the last access for every connected ip
    so the number of active users can be determined."""

    def _decorator(request: WSGIRequest) -> HttpResponse:
        # create a sessions if none exists (necessary for anonymous users)
        if not request.session or not request.session.session_key:
            request.session.save()

        request_ip = get_client_ip(request)
        last_requests = redis.get("last_requests")
        last_requests[request_ip] = time.time()
        redis.put("last_requests", last_requests)

        def check():
            active = redis.get("active_requests")
            if active > 0:
                leds.enable_act_led()
            else:
                leds.disable_act_led()

        redis.connection.incr("active_requests")
        check()
        response = func(request)
        redis.connection.decr("active_requests")
        check()

        return response

    return wraps(func)(_decorator)
