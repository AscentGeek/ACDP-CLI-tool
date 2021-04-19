from argparse import ArgumentParser, Action
from datetime import timezone, timedelta, datetime
import re


def _date_strftime_functer(format):
    def _(d):
        return d.strftime(format)

    return _


def _date_strptime_functer(format):
    def _(d):
        return datetime.strptime(d, format).date()

    return _


date_format = "%Y%m%d"
date_ftime = _date_strftime_functer(date_format)
date_ptime = _date_strptime_functer(date_format)


RE_DATE = re.compile(r"^\d{8}$")
RE_RANGED_DATE = re.compile(r"^\d{8}~\d{8}$")
KST = timezone(timedelta(hours=9))
KST_today = datetime.now(KST).date()
KST_today_str = date_ftime(KST_today)
KST_yesterday = KST_today - timedelta(days=1)
KST_yesterday_str = date_ftime(KST_yesterday)


def _filter_iter_functer(RE):
    def _(iter):
        return tuple([i for i in iter if RE.match(i)])

    return _


filter_date_list = _filter_iter_functer(RE_DATE)
filter_ranged_date_list = _filter_iter_functer(RE_RANGED_DATE)


def parse_ranged_date(ranged_date):
    st_date_str, en_date_str = ranged_date.split("~")
    st_date = datetime.strptime(st_date_str, date_format).date()
    en_date = datetime.strptime(en_date_str, date_format).date()
    range_dates = []
    if st_date > en_date:
        st_date, en_date = en_date, st_date
    range_dates = [
        st_date + timedelta(days=i) for i in range((en_date - st_date).days)
    ]
    return tuple(range_dates)


def parse_ranged_date_str(ranged_date):
    parsed = parse_ranged_date(ranged_date)
    return tuple([date_ftime(d) for d in parsed])


def parse_ranged_date_str_list(ranged_date_list):
    result = []
    for ranged_date in ranged_date_list:
        parsed = parse_ranged_date_str(ranged_date)
        result = [*result, *parsed]
    return tuple(result)


def filter_days_str_before_today(days_str_list):
    KST = timezone(timedelta(hours=9))
    KST_today = datetime.now(KST).date()
    return tuple([d for d in days_str_list if date_ptime(d) < KST_today])


def drop_duplicated_date(date_list):
    droped = set(date_list)
    return tuple(droped)


def parse_date_args(date_list):
    plain_list = filter_date_list(date_list)
    ranged_list = filter_ranged_date_list(date_list)
    parsed_ranged = parse_ranged_date_str_list(ranged_list)
    droped = drop_duplicated_date([*plain_list, *parsed_ranged])
    validated = filter_days_str_before_today(droped)
    return validated


class DateAction(Action):
    def __init__(self, option_strings, dest, nargs="*", **kwargs):
        if nargs != "*":
            # nargs는 *모드로 강제 됩니다
            nargs = "*"
        super(DateAction, self).__init__(
            option_strings, dest, nargs=nargs, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, parse_date_args(values))
