"""Baseline: synthesise DUO's dataset with synthpop-py's default settings and
measure how often the business rules are violated.

Usage (from the repository root):

    python scripts/baseline.py                  # 50,000 rows, seed 2834727 (as in DUO's notebook)
    python scripts/baseline.py --n 1291         # as many rows as the original

Writes to output/: the synthetic CSV, a JSON with all numbers and the package
versions, and a Markdown table.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from importlib.metadata import version
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rulecheck.evaluate import evaluate, markdown_table, to_json  # noqa: E402

DEFAULT_SEED = 2834727  # the seed in DUO's notebook
DEFAULT_N = 50_000  # DUO's notebook: many more rows than the original, so the flaws show


def versions() -> dict:
    out = {"python": platform.python_version()}
    for pkg in ("synthpop-py", "pandas", "scikit-learn", "numpy"):
        out[pkg] = version(pkg)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Baseline with synthpop-py (default settings).")
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "Synthetic_Homicide.csv")
    parser.add_argument("--n", type=int, default=DEFAULT_N, help="number of synthetic rows")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=ROOT / "output")
    args = parser.parse_args(argv)

    from synthpop import Synthesiser

    orig = pd.read_csv(args.data)
    t0 = time.time()
    syn = Synthesiser(random_seed=args.seed).fit(orig).generate(args.n)
    seconds = round(time.time() - t0, 1)

    args.out.mkdir(parents=True, exist_ok=True)
    stem = f"baseline_n{args.n}_seed{args.seed}"
    csv_path = args.out / f"{stem}.csv"
    syn.to_csv(csv_path, index=False)

    result = evaluate(orig, syn, label="baseline")
    payload = to_json(result) | {
        "settings": {"n": args.n, "seed": args.seed, "method": "synthpop-py defaults (CART)"},
        "synthesis_seconds": seconds,
        "versions": versions(),
        "file": csv_path.name,
    }
    (args.out / f"{stem}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    table = markdown_table([result])
    (args.out / f"{stem}.md").write_text(table, encoding="utf-8")

    print(f"Synthesis: {args.n} rows, seed {args.seed}, {seconds} s")
    print("Versions: " + ", ".join(f"{k} {v}" for k, v in payload["versions"].items()))
    print()
    print(table)
    print(f"Written to {args.out}: {stem}.csv, {stem}.json, {stem}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
