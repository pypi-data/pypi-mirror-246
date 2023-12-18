import time
import pytz
from datetime import datetime, timedelta

TIME_ZONE = "Etc/GMT+0"

# def get_timestamp() -> int:
#    return calendar.timegm(time.gmtime())


def get_timestamp() -> int:
    global TIME_ZONE
    # Obter o objeto de fuso horário para UTC-3
    tz_utc_minus3 = pytz.timezone(TIME_ZONE)

    # Obter a data e hora atual com o fuso horário UTC-3
    current_time_utc_minus3 = datetime.now(tz_utc_minus3)

    # Converter a data e hora para um timestamp
    timestamp = int(current_time_utc_minus3.timestamp())

    return timestamp


def date_to_timestamp(dt):
    return time.mktime(dt.timetuple())


def get_expiration_time_quotex(timestamp, duration):
    now_date = datetime.fromtimestamp(timestamp)
    shift = 0
    if now_date.second >= 30:
        shift = 1
    exp_date = now_date.replace(second=0, microsecond=0)
    exp_date = exp_date + timedelta(minutes=int(duration / 60) + shift)
    return int(date_to_timestamp(exp_date))


def get_expiration_time(timestamp, duration):
    now = datetime.now()
    new_date = now.replace(second=0, microsecond=0)
    exp = new_date + timedelta(seconds=duration)
    exp_date = exp.replace(second=0, microsecond=0)
    return int(date_to_timestamp(exp_date))


def get_period_time(duration):
    now = datetime.now()
    period_date = now - timedelta(seconds=duration)
    return int(date_to_timestamp(period_date))


def get_remaning_time(timestamp):
    now_date = datetime.fromtimestamp(timestamp)
    exp_date = now_date.replace(second=0, microsecond=0)
    if (int(date_to_timestamp(exp_date + timedelta(minutes=1))) - timestamp) > 30:
        exp_date = exp_date + timedelta(minutes=1)
    else:
        exp_date = exp_date + timedelta(minutes=2)
    exp = []
    for _ in range(5):
        exp.append(date_to_timestamp(exp_date))
        exp_date = exp_date + timedelta(minutes=1)
    idx = 11
    index = 0
    now_date = datetime.fromtimestamp(timestamp)
    exp_date = now_date.replace(second=0, microsecond=0)
    while index < idx:
        if int(exp_date.strftime("%M")) % 15 == 0 and (int(date_to_timestamp(exp_date)) - int(timestamp)) > 60 * 5:
            exp.append(date_to_timestamp(exp_date))
            index = index + 1
        exp_date = exp_date + timedelta(minutes=1)

    remaning = []

    for idx, t in enumerate(exp):
        if idx >= 5:
            dr = 15 * (idx - 4)
        else:
            dr = idx + 1
        remaning.append((dr, int(t) - int(time.time())))

    return remaning
