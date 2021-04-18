from argparse import ArgumentParser, Action
from datetime import timezone, timedelta, datetime
import re

RE_DATE = re.compile(r"^\d{8}$")
RE_DATE_RANGE = re.compile(r"^\d{8}~\d{8}$")

date_format = "%Y%m%d"
KST = timezone(timedelta(hours=9))
today = datetime.now(KST).date()
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime(date_format)


class FooAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(FooAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print("%r %r %r" % (namespace, values, option_string))
        setattr(namespace, self.dest, values)


class DateAction(Action):
    def __init__(self, option_strings, dest, nargs="*", **kwargs):
        if nargs != "*":
            print(f"{option_strings}의 nargs는 *모드로 강제 됩니다.")
            nargs = "*"
        super(DateAction, self).__init__(
            option_strings, dest, nargs=nargs, **kwargs
        )

    def parse_date_range(date_range_str):
        st_date_str, en_date_str = date_range_str.split("~")
        st_date = datetime.strptime(st_date_str, date_format).date()
        en_date = datetime.strptime(en_date_str, date_format).date()
        range_dates = []
        if en_date == st_date:
            range_dates.append(st_date)
        else:
            if st_date > en_date:
                st_date, en_date = en_date, st_date
            range_dates = [
                st_date + timedelta(days=i)
                for i in range((en_date - st_date).days)
            ]
        return range_dates

    def get_date_range_list(dates):
        return [date for date in dates if RE_DATE_RANGE.match(date)]

    def get_date_list(dates):
        return [date for date in dates if RE_DATE.match(date)]

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


parser = ArgumentParser()
parser.add_argument(
    "-d", "--date", action=DateAction, dest="date_list", nargs="?"
)
args = parser.parse_args()
print(args)


"""
parser = ArgumentParser(description="ACDP Kakao Clix CLI tool")
parser.add_argument(
    "-a",
    "--apikey",
    action="store",
    help="API 액세스 키.",
)
parser.add_argument("-c", "--company", action="store", help="고객사 이름.")
parser.add_argument(
    "-d",
    "--dates",
    action="append",
    dest="date_list",
    default=yesterday_str,
    help="YYYYMMDD 형식의 단일 일자. 여러번 호출 시 리스트 형태로 누적 됩니다.",
)

args = parser.parse_args()
print(args.accumulate(args.integers))

# https://greeksharifa.github.io/references/2019/02/12/argparse-usage/#dest-%EC%A0%81%EC%9A%A9-%EC%9C%84%EC%B9%98-%EC%A7%80%EC%A0%95
"""