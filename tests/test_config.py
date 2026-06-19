def test_config_roundtrip(Rough Cut, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    Rough Cut["save_config"]({"fmt": "GIF", "crf": 18, "out_dir": "C:/clips"})
    assert Rough Cut["load_config"]() == {"fmt": "GIF", "crf": 18, "out_dir": "C:/clips"}


def test_config_missing_is_empty(Rough Cut, tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "does_not_exist"))
    assert Rough Cut["load_config"]() == {}
