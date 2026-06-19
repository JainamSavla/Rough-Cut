def test_even(Rough Cut):
    assert Rough Cut["even"](721) == 720
    assert Rough Cut["even"](720) == 720
    assert Rough Cut["even"](0) == 0


def test_fmt_and_parse_roundtrip(Rough Cut):
    assert Rough Cut["parse_time"]("1:02:03.250") == 3723.25
    assert Rough Cut["fmt_time"](3723.25) == "1:02:03.250"


def test_parse_time_forms(Rough Cut):
    assert Rough Cut["parse_time"]("90.5") == 90.5
    assert Rough Cut["parse_time"]("01:15.250") == 75.25
    assert Rough Cut["parse_time"]("") is None
