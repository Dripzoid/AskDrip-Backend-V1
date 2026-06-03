from typing import Any, Optional
from time import time


def success_response(
    message: str,
    data: Optional[Any] = None,
    route: Optional[str] = None,
    start_time: Optional[float] = None
):

    response_time = None

    # CALCULATE RESPONSE TIME
    if start_time is not None:

        response_time = (
            f"{round(time() - start_time, 2)} sec"
        )

    return {
        "success": True,
        "message": message,
        "route": route,
        "response_time": response_time,
        "data": data
    }


def error_response(
    message: str,
    route: Optional[str] = None
):

    return {
        "success": False,
        "message": message,
        "route": route,
        "response_time": None,
        "data": None
    }