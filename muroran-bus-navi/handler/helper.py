from logging import getLogger

from bottle import request

import pendulum

logger = getLogger(__name__)


def parse_param_date_time(
    default=pendulum.now,
    tz="Asia/Tokyo",
    date_param_name="date",
    time_param_name="time",
):
    default = default(tz) if callable(default) else default

    date = request.params.get(date_param_name, default.to_date_string())
    time = request.params.get(time_param_name, default.format("HH:mm"))

    return pendulum.parse(f"{date} {time}", tz=tz)
