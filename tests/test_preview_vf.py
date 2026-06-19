# Pure tests for build_preview_vf — no GUI, no mpv.
def make(Rough Cut, **kw):
    base = dict(input_path="in.mp4", output_path="out.mp4",
                src_w=1920, src_h=1080, start=2.0, end=8.0)
    base.update(kw)
    return Rough Cut["ExportSettings"](**base)


def vf_props(Rough Cut, **kw):
    return Rough Cut["build_preview_vf"](make(Rough Cut, **kw))


def test_empty_settings_minimal(Rough Cut):
    vf, props = vf_props(Rough Cut)
    assert "crop=" not in vf and "eq=" not in vf
    assert props.get("speed", 1.0) == 1.0


def test_crop_orient_color(Rough Cut):
    vf, _ = vf_props(Rough Cut, crop=(10, 20, 1280, 720), rotate=90,
                     flip_h=True, brightness=0.2, contrast=1.1, saturation=1.2)
    assert "crop=1280:720:10:20" in vf
    assert "transpose=1" in vf and "hflip" in vf
    assert "eq=brightness=0.200:contrast=1.100:saturation=1.200" in vf


def test_grayscale_denoise_sharpen(Rough Cut):
    vf, _ = vf_props(Rough Cut, grayscale=True, denoise=True, sharpen=True)
    assert "hue=s=0" in vf and "hqdn3d" in vf and "unsharp" in vf


def test_text_not_in_mpv_vf(Rough Cut):
    # mpv can't do drawtext; text previews on the still, not the live vf
    vf, _ = vf_props(Rough Cut, text="Hello")
    assert "drawtext" not in vf


def test_fades_use_absolute_timeline(Rough Cut):
    # mpv plays from s.start, so fade st must be source-absolute
    vf, _ = vf_props(Rough Cut, start=2.0, end=8.0, fade_in=1.0, fade_out=1.5)
    assert "fade=t=in:st=2.00:d=1.00" in vf
    assert "fade=t=out:st=6.50:d=1.50" in vf


def test_watermark_not_in_mpv_vf(Rough Cut):
    # watermark overlay previews on the still (ffmpeg), not the mpv vf
    vf, _ = vf_props(Rough Cut, watermark_path="logo.png", watermark_pos="br")
    assert "movie=" not in vf and "overlay=" not in vf


def test_audio_props(Rough Cut):
    _, props = vf_props(Rough Cut, speed=2.0, volume=1.5, mute=True)
    assert props["speed"] == 2.0
    assert abs(props["volume"] - 150.0) < 0.01      # mpv volume is 0-100(+)
    assert props["mute"] is True


def test_subtitles_use_native_sub_file(Rough Cut):
    _, props = vf_props(Rough Cut, subtitles_path="subs.srt")
    assert props["sub-file"] == "subs.srt"


def test_non_live_effects_omitted(Rough Cut):
    vf, props = vf_props(Rough Cut, reverse=True, boomerang=True, stabilize=True,
                         target_size_mb=10.0)
    assert "vidstab" not in vf and "reverse" not in vf
    # scale is omitted too (mpv fits the window)
    assert "scale=" not in vf


def test_still_vf_adjustments_and_overlays(Rough Cut):
    chain = Rough Cut["build_still_vf"](make(
        Rough Cut, brightness=0.2, grayscale=True, denoise=True, sharpen=True,
        text="Hi"))
    j = ",".join(chain)
    assert "eq=" in j and "hue=s=0" in j and "hqdn3d" in j and "unsharp" in j
    assert "drawtext=" in j


def test_still_vf_excludes_geometry(Rough Cut):
    chain = Rough Cut["build_still_vf"](make(Rough Cut, crop=(0, 0, 640, 480),
                                         rotate=90, flip_h=True))
    j = ",".join(chain)
    assert "crop=" not in j and "transpose" not in j and "hflip" not in j


def test_sha256_file(Rough Cut, tmp_path):
    import hashlib
    p = tmp_path / "x.bin"
    p.write_bytes(b"Rough Cut")
    assert Rough Cut["_sha256_file"](str(p)) == hashlib.sha256(b"Rough Cut").hexdigest()


def test_mpv_download_spec_pinned(Rough Cut):
    spec = Rough Cut["MPV_DOWNLOAD"]
    assert spec["url"].startswith("https://")
    assert len(spec["sha256"]) == 64
    assert spec["member"] == "libmpv-2.dll"


def test_parse_fps(Rough Cut):
    assert Rough Cut["parse_fps"]("30000/1001") == 29.97
    assert Rough Cut["parse_fps"]("25/1") == 25.0
    assert Rough Cut["parse_fps"]("0/0") is None
    assert Rough Cut["parse_fps"](None) is None


def test_stream_rotation(Rough Cut):
    sr = Rough Cut["stream_rotation"]
    assert sr({"side_data_list": [{"rotation": -90}]}) == 90
    assert sr({"side_data_list": [{"rotation": -180}]}) == 180
    assert sr({"tags": {"rotate": "270"}}) == 270
    assert sr({}) == 0
