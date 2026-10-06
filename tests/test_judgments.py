import textwrap

import pytest

from ptcg import judgments as J


def _write(root, name, text):
    p = root / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text), encoding="utf-8")
    return p


@pytest.fixture
def repo(tmp_path):
    _write(tmp_path, "data/judgments/deck.yaml", """\
        deck: dragapult-ex
        judgments:
          - id: dpx-mir-01
            vs: dragapult-ex
            text: lock items second
            confidence: 0.6
            window: TEF-30C
            depends_on: [Budew]
            where: guide.md
          - id: dpx-mir-02
            text: the other line
            confidence: 0.55
            weight: 2
            window: TEF-30C
            alternative_to: dpx-mir-01
            where: guide.md
        """)
    _write(tmp_path, "data/judgments/sources/2026-10-05_log_a.yaml", """\
        kind: log
        date: 2026-10-05
        ref: a.md
        window: TEF-30C
        observations:
          - {judgment: dpx-mir-01, result: held}
          - {judgment: dpx-mir-01, result: failed}
          - {judgment: dpx-mir-02, result: n/a}
        """)
    _write(tmp_path, "data/judgments/sources/2026-10-06_feedback_s.yaml", """\
        kind: feedback
        date: 2026-10-06
        ref: raw/s.md
        reviewer: S
        window: TEF-30C
        observations:
          - {judgment: dpx-mir-01, result: disagree}
        claims:
          - {id: c1, type: 备选路线, text: bench two, status: 待验证, depends_on: [Budew]}
        """)
    _write(tmp_path, "guide.md", "a（信心 60%，dpx-mir-01）b（信心 55%，dpx-mir-02）\n")
    return tmp_path


def _load(root):
    return J.load_judgments(root / "data/judgments"), J.load_sources(root / "data/judgments/sources")


def test_confidence_counts_games_fully_and_feedback_half(repo):
    js, ss = _load(repo)
    rows = J.history("dpx-mir-01", js["dpx-mir-01"], ss)
    # (0.6*4 + 1 + 0 + 0) / (4 + 1 + 1 + 0.5)
    assert J.confidence(js["dpx-mir-01"], rows) == pytest.approx(3.4 / 6.5)
    assert J.history("dpx-mir-02", js["dpx-mir-02"], ss) == []


def test_check_and_sync_marks(repo):
    js, ss = _load(repo)
    errors, warnings = J.check(js, ss, root=repo)
    assert errors == []
    assert any("dpx-mir-01 marked 60%, now 50%" in w for w in warnings)
    assert J.sync(js, ss, root=repo) == ["guide.md"]
    assert "（信心 50%，dpx-mir-01）" in (repo / "guide.md").read_text(encoding="utf-8")
    assert J.check(js, ss, root=repo)[1] == []


def test_check_catches_bad_input(repo):
    _write(repo, "data/judgments/sources/2026-10-07_video_b.yaml", """\
        kind: video
        date: 2026-10-07
        ref: b.md
        window: TEF-30C
        observations:
          - {judgment: nope, result: held}
          - {judgment: dpx-mir-01, result: agree}
        claims:
          - {id: c2, type: 灵感, text: x, status: 已转正}
        """)
    (repo / "guide.md").write_text("（信心 60%，dpx-mir-01）（信心 50%，ghost-01）\n", encoding="utf-8")
    js, ss = _load(repo)
    errors = "\n".join(J.check(js, ss, root=repo)[0])
    assert "unknown judgment nope" in errors
    assert "result 'agree'" in errors
    assert "type '灵感'" in errors
    assert "promoted_to" in errors
    assert "unknown judgment ghost-01" in errors
    assert "no （信心 …，dpx-mir-02） mark" in errors


def test_stale_when_card_leaves_standard(repo, monkeypatch):
    monkeypatch.setattr(J, "_standard_names", lambda: frozenset())
    monkeypatch.setattr(J, "_in_lists", lambda window, slug: None)
    js, ss = _load(repo)
    out = J.stale(js, ss, "TEF-30C")
    assert any(x.startswith("dpx-mir-01") and "Budew 已不在 Standard" in x for x in out)
    assert any(x.startswith("c1") for x in out)


def test_stale_when_usage_shifts(repo, monkeypatch):
    monkeypatch.setattr(J, "_standard_names", lambda: frozenset({"Budew"}))
    lists = {"OLD": {"Budew": 0.9}, "NEW": {}}
    monkeypatch.setattr(J, "_in_lists", lambda window, slug: lists.get(window))
    js, ss = _load(repo)
    js["dpx-mir-01"]["window"] = "OLD"
    out = J.stale(js, ss, "NEW")
    assert out == ["dpx-mir-01（OLD）：lock items second —— dragapult-ex 的卡表带 Budew 的比例 90% → <25%"]


def test_calibration_scores_each_game_at_the_confidence_before_it(repo):
    js, ss = _load(repo)
    lines = J.calibration(js, ss)
    # held at 0.6, then failed at (0.6*4 + 1) / 5 = 0.68; feedback is not scored
    assert "| 60–69% | 2 | 50% |" in lines
    assert any("Brier 分数 0.311（2 次判定" in l for l in lines)


def test_repo_data_is_valid():
    errors, _ = J.check(J.load_judgments(), J.load_sources())
    assert errors == []
