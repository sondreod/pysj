from pysj import seconds


def test_hours():
    assert seconds(hours=1) == 3600


def test_quarters():
    assert seconds(quarters=2) == 15768000  # 182 days and 12 hours


def test_milliseconds_less_than_a_second():
    assert seconds(milliseconds=400) == 0


def test_milliseconds_more_than_a_second_less_than_two():
    assert seconds(milliseconds=1999) == 1


def test_large_return_value():
    assert seconds(years=1999) == 63040464000


def test_time_interval_composition():
    assert (
        seconds(
            hours=1,
            months=1,
            days=1,
            years=1,
            minutes=1,
            weeks=1,
            quarters=1,
            seconds=1,
        )
        == 42706861
    )


def test_interval_comparison_quarter_in_year():
    assert seconds(quarters=4) == seconds(years=1)


def test_interval_comparison_days_in_year():
    assert seconds(days=365) == seconds(years=1)
