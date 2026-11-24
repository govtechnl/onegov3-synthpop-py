"""Compare synthetic datasets: business rule violations and S_pMSE per dataset.

Usage (from the repository root):

    python scripts/evaluate.py output/nulmeting_n50000_seed2834727.csv output/mijn_aanpak.csv

The first file is the reference (usually the nulmeting). For every next file the
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
    parser = argparse.ArgumentParser(description="Vergelijk synthetische datasets op regels en kwaliteit.")
    parser.add_argument("csv", type=Path, nargs="+", help="een of meer synthetische CSV's; de eerste is de referentie")
    parser.add_argument("--labels", nargs="+", help="namen voor de kolommen in de tabel (standaard: bestandsnamen)")
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "Synthetic_Homicide.csv")
    parser.add_argument("--md", type=Path, help="schrijf de vergelijking als Markdown naar dit bestand")
    parser.add_argument("--json", type=Path, help="schrijf alle getallen als JSON naar dit bestand")
    parser.add_argument("--top", type=int, default=10, help="aantal kolomparen in de lijst met grootste verslechtering")
    args = parser.parse_args(argv)

    labels = args.labels or [p.stem for p in args.csv]
    if len(labels) != len(args.csv):
        parser.error("geef evenveel --labels als bestanden")
    if len(set(labels)) != len(labels):
        parser.error("labels moeten uniek zijn")

    orig = pd.read_csv(args.data)
    results = [evaluate(orig, pd.read_csv(p), label=lab) for p, lab in zip(args.csv, labels, strict=True)]

    out = [markdown_table(results)]
    sizes = {r["rijen"] for r in results}
    if len(sizes) > 1:
        out.append(
            "LET OP: de datasets hebben een verschillend aantal rijen. "
            "Vergelijk S_pMSE alleen bij gelijke aantallen.\n"
        )
    for other in results[1:]:
        changes = biggest_changes(results[0], other, top=args.top)
        out.append(f"\nKolomparen waar de S_pMSE het meest steeg van {results[0]['label']} naar {other['label']}:\n")
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
