from datetime import date

import pytest

from ptcg_video import cli
from ptcg_video.cardpool import find_data_dir, load_pool, parse_date, season_for


def test_parse_date():
    assert parse_date("20260830") == date(2026, 8, 30)
    assert parse_date("2026-08-30T10:00:00") == date(2026, 8, 30)
    assert parse_date(None) is None


def test_season_for_dates(data_dir):
    assert season_for(data_dir, date(2026, 8, 30)) == "2026-27"
    assert season_for(data_dir, date(2026, 4, 9)) == "2025-26"
    assert season_for(data_dir, date(2026, 4, 10)) == "2026-27"
    # TCG Live rotates earlier.
    assert season_for(data_dir, date(2026, 3, 30), live=True) == "2026-27"
    assert season_for(data_dir, None) == "2026-27"
    with pytest.raises(ValueError):
        season_for(data_dir, date(2020, 1, 1))


def test_load_pool_dedupes_names(data_dir):
    pool = load_pool(data_dir, "2025-26")
    assert pool.names == ["Charizard ex", "Iono", "Judge"]
    assert pool.supertypes["Iono"] == "Trainer"
    with pytest.raises(FileNotFoundError):
        load_pool(data_dir, "1999-00")


def test_find_data_dir(data_dir, tmp_path):
    nested = data_dir.parent / "video" / "out"
    nested.mkdir(parents=True)
    assert find_data_dir(tmp_path / "nowhere", nested) == data_dir


def test_cli_auto_pool_from_upload_date(data_dir, tmp_path):
    srt = tmp_path / "m.en.srt"
    srt.write_text("1\n00:00:01,000 --> 00:00:03,000\nDragapult ex and Charizard ex, judge says Judge\n",
                   encoding="utf-8")
    (tmp_path / "m.info.json").write_text('{"id": "m", "upload_date": "20260830"}', encoding="utf-8")
    out = tmp_path / "out"
    assert cli.main(["analyze", str(srt), "--captions-only", "--captions", str(srt), "--no-llm",
                     "--data-dir", str(data_dir), "--out", str(out)]) == 0
    report = (out / "m" / "report.md").read_text(encoding="utf-8")
    # 2026-27 pool: Dragapult ex yes, Charizard ex (2025-26 only) no, lowercase "judge" no.
    assert "| Dragapult ex | 1 |" in report
    assert "Charizard" not in report.split("## Cards mentioned")[1]
    assert "| Judge | 1 |" in report


def test_cli_format_override_and_none(data_dir, tmp_path):
    srt = tmp_path / "m.en.srt"
    srt.write_text("1\n00:00:01,000 --> 00:00:03,000\nCharizard ex attacks\n", encoding="utf-8")
    out = tmp_path / "out"
    cli.main(["analyze", str(srt), "--captions-only", "--captions", str(srt), "--no-llm",
              "--data-dir", str(data_dir), "--format", "2025-26", "--out", str(out)])
    assert "| Charizard ex | 1 |" in (out / "m" / "report.md").read_text(encoding="utf-8")
    cli.main(["analyze", str(srt), "--captions-only", "--captions", str(srt), "--no-llm",
              "--cards", "none", "--out", str(out)])
    assert "Cards mentioned" not in (out / "m" / "report.md").read_text(encoding="utf-8")


def test_pool_reads_files_saved_with_bom(data_dir):
    path = data_dir / "formats" / "2025-26" / "card_pool.csv"
    path.write_text("\ufeff" + path.read_text(encoding="utf-8"), encoding="utf-8")
    assert "Iono" in load_pool(data_dir, "2025-26").names


def _srt(tmp_path, text="Charizard ex attacks"):
    srt = tmp_path / "m.en.srt"
    srt.write_text(f"1\n00:00:01,000 --> 00:00:03,000\n{text}\n", encoding="utf-8")
    return srt


def test_format_beats_card_env(data_dir, tmp_path, monkeypatch):
    names = tmp_path / "names.txt"
    names.write_text("Pikachu\n", encoding="utf-8")
    monkeypatch.setenv("PTCG_CARD_NAMES", str(names))
    srt, out = _srt(tmp_path), tmp_path / "out"
    cli.main(["analyze", str(srt), "--captions-only", "--captions", str(srt), "--no-llm",
              "--data-dir", str(data_dir), "--format", "2025-26", "--out", str(out)])
    assert "| Charizard ex | 1 |" in (out / "m" / "report.md").read_text(encoding="utf-8")


def test_broken_data_dir_skips_card_names(data_dir, tmp_path, capsys):
    (data_dir / "formats" / "standard_rotations.json").write_text("{not json", encoding="utf-8")
    srt, out = _srt(tmp_path), tmp_path / "out"
    assert cli.main(["analyze", str(srt), "--captions-only", "--captions", str(srt), "--no-llm",
                     "--data-dir", str(data_dir), "--out", str(out)]) == 0
    assert "card names: skipped" in capsys.readouterr().err
    assert "Cards mentioned" not in (out / "m" / "report.md").read_text(encoding="utf-8")


def test_bad_region_spec_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as e:
        cli.build_parser().parse_args(["analyze", "x.mp4", "--hash-regions", "0.5,0.5"])
    assert e.value.code == 2
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["analyze", "x.mp4", "--frames-per-window", "0"])
