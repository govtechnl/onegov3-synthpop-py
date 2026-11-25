"""Compare synthetic datasets: business rule violations and S_pMSE per dataset.

Usage (from the repository root):

    python scripts/evaluate.py output/baseline_n50000_seed2834727.csv output/my_approach.csv

The first file is the reference (usually the baseline). For every next file the
script also lists the column pairs whose S_pMSE got worse the most. Use --md and
--json to save the results, for example for your pitch.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rulecheck.evaluate import biggest_changes, evaluate, frame_to_markdown, markdown_table, to_json  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare synthetic datasets on rules and quality.")
    parser.add_argument("csv", type=Path, nargs="+", help="one or more synthetic CSVs; the first is the reference")
    parser.add_argument("--labels", nargs="+", help="column names for the table (default: file names)")
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "Synthetic_Homicide.csv")
    parser.add_argument("--md", type=Path, help="write the comparison as Markdown to this file")
    parser.add_argument("--json", type=Path, help="write all numbers as JSON to this file")
    parser.add_argument("--top", type=int, default=10, help="number of column pairs in the list of largest declines")
    args = parser.parse_args(argv)

    labels = args.labels or [p.stem for p in args.csv]
    if len(labels) != len(args.csv):
        parser.error("give as many --labels as files")
    if len(set(labels)) != len(labels):
        parser.error("labels must be unique")

    orig = pd.read_csv(args.data)
    results = [evaluate(orig, pd.read_csv(p), label=lab) for p, lab in zip(args.csv, labels, strict=True)]

    out = [markdown_table(results)]
    sizes = {r["rows"] for r in results}
    if len(sizes) > 1:
        out.append(
            "NOTE: the datasets have different numbers of rows. Use the baseline settings (50,000 rows) to compare.\n"
        )
    for other in results[1:]:
        changes = biggest_changes(results[0], other, top=args.top)
        out.append(f"\nColumn pairs whose S_pMSE increased most from {results[0]['label']} to {other['label']}:\n")
        out.append(frame_to_markdown(changes))
        out.append("\n")
    text = "\n".join(out)
    print(text)

    if args.md:
        args.md.parent.mkdir(parents=True, exist_ok=True)
        args.md.write_text(text, encoding="utf-8")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps([to_json(r) for r in results], ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
