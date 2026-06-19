def test_parse_version(Rough Cut):
    f = Rough Cut["_parse_version"]
    assert f("v2.4.1") == (2, 4, 1)
    assert f("2.5") == (2, 5)
    assert f("v3") == (3,)
    assert f("") == ()
    assert f("garbage") == ()
    assert f(None) == ()


def test_is_newer(Rough Cut):
    f = Rough Cut["_is_newer"]
    assert f("v2.5", "2.4.1") is True
    assert f("2.4.1", "2.4.1") is False
    assert f("2.4", "2.4.1") is False
    assert f("v2.10", "v2.9") is True
    assert f("2.5", "2.5.0") is False


def test_latest_tag_from_json(Rough Cut):
    f = Rough Cut["_latest_tag_from_json"]
    assert f({"tag_name": "v2.5"}) == "v2.5"
    assert f({}) is None
    assert f({"tag_name": ""}) is None
    assert f([]) is None
