import datetime

from pysj import months_in_interval

periods = list(
    months_in_interval(datetime.datetime(2020, 1, 1), datetime.datetime(2023, 4, 6))
)


def test_number_of_periods():
    assert 12 * 3 + 4 == len(periods)


def test_number_of_periods_inclusive_on_both_ends():
    assert periods[0] == (1, 2020)
    assert periods[-1] == (4, 2023)


def test_months_in_interval_with_period_equal_one_day():
    periods = list(
        months_in_interval(datetime.datetime(2023, 1, 1), datetime.datetime(2023, 1, 1))
    )

    assert periods == [(1, 2023)]


def test_months_in_interval_with_leap_year():
    periods = list(
        months_in_interval(
            datetime.datetime(1999, 12, 31), datetime.datetime(2000, 2, 29)
        )
    )

    assert periods[0] == (12, 1999)
    assert periods[-1] == (2, 2000)
    assert len(periods) == 3
