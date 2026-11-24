import json
import subprocess
import sys

import pytest

from conftest import DATA, ROOT, SAMPLE
from rulecheck.__main__ import main


def test_cli_table(capsys):
    assert main([str(SAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "violations" in out
    assert "Rows with at least 1 violation" in out


def test_cli_strict_and_json(capsys):
    assert main([str(DATA), "--strict"]) == 0
    capsys.readouterr()
    assert main([str(SAMPLE), "--strict", "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["rows"] == 554
    assert {item["rule"] for item in data["rules"]} >= {"1", "2", "6.4"}


def test_cli_rejects_wrong_columns(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("a,b\n1,2\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        main([str(bad)])


def test_baseline_and_evaluate_scripts(tmp_path):
    pytest.importorskip("synthpop")
    run = [sys.executable, str(ROOT / "scripts" / "baseline.py"), "--n", "400", "--out", str(tmp_path)]
    subprocess.run(run, check=True, capture_output=True, text=True)
    stem = "baseline_n400_seed2834727"
    for ext in ("csv", "json", "md"):
        assert (tmp_path / f"{stem}.{ext}").exists()
    payload = json.loads((tmp_path / f"{stem}.json").read_text(encoding="utf-8"))
    assert payload["rows"] == 400
    assert payload["spmse"]["pairs"] == 253  # 22 columns: 22 * 23 / 2 pairs

    md = tmp_path / "comparison.md"
    run = [
        sys.executable, str(ROOT / "scripts" / "evaluate.py"),
        str(tmp_path / f"{stem}.csv"), str(SAMPLE),
        "--labels", "baseline", "sample", "--md", str(md), "--json", str(tmp_path / "c.json"),
    ]
    result = subprocess.run(run, check=True, capture_output=True, text=True)
    assert "| Rule | Description | baseline | sample |" in result.stdout
    assert "NOTE: the datasets have different numbers of rows" in result.stdout
    assert md.exists()
    assert len(json.loads((tmp_path / "c.json").read_text(encoding="utf-8"))) == 2
