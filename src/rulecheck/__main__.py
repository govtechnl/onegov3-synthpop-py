"""Command line: python -m rulecheck <file.csv> [--json] [--strict]

Prints, per business rule, how many rows of a (synthetic) dataset violate it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from .rules import COLUMNS, any_violation, check_rules


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m rulecheck",
        description="Toets een dataset aan de business rules van de synthpop.py-challenge.",
    )
    parser.add_argument("csv", type=Path, help="pad naar een CSV met dezelfde kolommen als de dataset van DUO")
    parser.add_argument("--json", action="store_true", help="geef het resultaat als JSON")
    parser.add_argument("--strict", action="store_true", help="exitcode 1 als er minstens één overtreding is")
    args = parser.parse_args(argv)

    df = pd.read_csv(args.csv)
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        parser.error(f"kolommen ontbreken in {args.csv}: {missing}")

    report = check_rules(df)
    n_any = int(any_violation(df).sum())
    n = len(df)

    if args.json:
        out = {
            "bestand": str(args.csv),
            "rijen": n,
            "rijen_met_overtreding": n_any,
            "regels": report.to_dict(orient="records"),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"{args.csv}: {n} rijen")
        print(report.to_string(index=False))
        share = 100 * n_any / n if n else 0.0
        print(f"Rijen met minstens 1 overtreding: {n_any} van {n} ({share:.2f}%)")

    return 1 if (args.strict and n_any) else 0


if __name__ == "__main__":
    sys.exit(main())
