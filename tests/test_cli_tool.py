from cli_tool import __version__
from cli_tool.DateAction import (
    filter_ranged_date_list,
    filter_date_list,
    parse_ranged_date_str,
    parse_ranged_date_str_list,
    filter_days_str_before_today,
    drop_duplicated_date,
    parse_date_args,
    DateAction,
)


def test_version():
    assert __version__ == "0.1.0"


def test_filter_date_list():
    target = "20200301"
    test_list = tuple([target, "2020-03-01", "asdf"])
    result_list = filter_date_list(test_list)
    assert len(result_list) == 1
    assert result_list[0] == target


def test_filter_date_list_empty():
    test_list = tuple(["2020-03-01", "asdf"])
    result_list = filter_date_list(test_list)
    assert len(result_list) == 0


def test_filter_ranged_date_list():
    target = "20200301~20200401"
    test_list = tuple([target, "2020-03-01~2020-04-01", "asdf"])
    result_list = filter_ranged_date_list(test_list)
    assert len(result_list) == 1
    assert result_list[0] == target


def test_filter_ranged_date_list_empty():
    test_list = tuple(["2020-03-01~2020-04-01", "asdf"])
    result_list = filter_ranged_date_list(test_list)
    assert len(result_list) == 0


def test_parse_ranged_date_str_reverse():
    ranged_date = "20200404~20200401"
    target = tuple(["20200401", "20200402", "20200403"])
    result = parse_ranged_date_str(ranged_date)
    for i, d in enumerate(target):
        assert result[i] == d


def test_parse_ranged_date_str():
    ranged_date = "20200401~20200404"
    target = tuple(["20200401", "20200402", "20200403"])
    result = parse_ranged_date_str(ranged_date)
    for i, d in enumerate(target):
        assert result[i] == d


def test_parse_ranged_date_str_empty():
    ranged_date = "20200401~20200401"
    result = parse_ranged_date_str(ranged_date)
    assert len(result) == 0


def test_parse_ranged_date_str_list():
    ranged_date_list = ["20200401~20200404", "20200301~20200304"]
    target = tuple(
        [
            "20200401",
            "20200402",
            "20200403",
            "20200301",
            "20200302",
            "20200303",
        ]
    )
    result = parse_ranged_date_str_list(ranged_date_list)
    for i, d in enumerate(target):
        assert result[i] == d


def test_parse_ranged_date_str_list_empty():
    ranged_date_list = []
    result = parse_ranged_date_str_list(ranged_date_list)
    assert len(result) == 0


def test_filter_days_str_before_today():
    date_list = tuple(["20210418", "20210419", "20210420"])
    target = date_list[0:1]
    result = filter_days_str_before_today(date_list)
    for i, d in enumerate(target):
        assert result[i] == d


def test_drop_duplicated_date():
    date_list = tuple(["20210418", "20210419"])
    date_list_2 = tuple([*date_list, "20210420"])
    target = tuple([*date_list_2])
    result = drop_duplicated_date([*date_list, *date_list_2])
    assert len(target) == len(result)
    for d in target:
        assert d in result


def test_parse_date_args():
    date_list = tuple(
        [
            "20210418",
            "20210419",
            "20210420",
            "20210417~20210422",
            "2021-03-01",
            "asdf",
            "20210303",
            "20210322",
        ]
    )
    target = ["20210417", "20210418", "20210303", "20210322"]
    result = parse_date_args(date_list)
    assert len(result) == len(target)
    for d in target:
        assert d in result


def test_DateAction():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-d", "--date", action=DateAction)
    target = ["20210417", "20210418", "20210303", "20210322"]
    args = parser.parse_args(
        "-d 20210418 20210419 20210420 20210417~20210422 2021-03-01 asdf 20210303 20210322".split()
    )
    arg_dict = dict(args._get_kwargs())

    assert len(arg_dict["date"]) == len(target)
    for d in target:
        assert d in arg_dict["date"]
