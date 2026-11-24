"""Evaluate a synthetic dataset: business rule violations and statistical quality.

Violations come from :mod:`rulecheck.rules`. Quality is measured with the
pairwise S_pMSE from synthpop-py (``synthpop.utility_metrics.pairwise_spmse``):
lower is better. S_pMSE depends strongly on the number of synthetic rows, so only
compare datasets with the same number of rows (and the same original data).
"""

from __future__ import annotations

import warnings

import pandas as pd

from .rules import COLUMNS, RULES, any_violation, violations


def check_columns(df: pd.DataFrame, name: str = "dataset") -> None:
    """Raise a clear error if ``df`` does not have exactly the 22 expected columns."""
    missing = [c for c in COLUMNS if c not in df.columns]
    extra = [c for c in df.columns if c not in COLUMNS]
    if missing or extra:
        raise ValueError(f"{name}: missing columns {missing}, unexpected columns {extra}")


def pairwise_quality(orig: pd.DataFrame, syn: pd.DataFrame) -> pd.DataFrame:
    """Pairwise S_pMSE between ``orig`` and ``syn`` (one row per column pair)."""
    from synthpop.utility_metrics import pairwise_spmse

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return pairwise_spmse(orig[COLUMNS], syn[COLUMNS])


def evaluate(orig: pd.DataFrame, syn: pd.DataFrame, label: str = "synthetic") -> dict:
    """Violations per rule and an S_pMSE summary for one synthetic dataset."""
    check_columns(orig, "original")
    check_columns(syn, label)
    n = len(syn)
    masks = violations(syn)
    n_any = int(any_violation(syn).sum())
    spmse = pairwise_quality(orig, syn)
    values = spmse["S_pMSE"].astype(float)
    return {
        "label": label,
        "rows": n,
        "rules": [
            {
                "rule": rule.id,
                "description": rule.name,
                "violations": int(masks[rule.id].sum()),
                "percentage": round(100 * int(masks[rule.id].sum()) / n, 2) if n else 0.0,
            }
            for rule in RULES
        ],
        "rows_with_violation": n_any,
        "percentage_rows_with_violation": round(100 * n_any / n, 2) if n else 0.0,
        "spmse": {
            "pairs": int(len(values)),
            "mean": round(float(values.mean()), 3),
            "median": round(float(values.median()), 3),
            "p90": round(float(values.quantile(0.9)), 3),
            "max": round(float(values.max()), 3),
        },
        "_spmse_table": spmse,
    }


def markdown_table(results: list[dict]) -> str:
    """A comparison table (Markdown) for one or more evaluation results."""
    head = "| Rule | Description | " + " | ".join(r["label"] for r in results) + " |"
    sep = "|---|---|" + "---:|" * len(results)
    lines = [head, sep]
    for i, rule in enumerate(RULES):
        cells = []
        for r in results:
            item = r["rules"][i]
            cells.append(f"{item['violations']:,} ({item['percentage']:.2f}%)")
        lines.append(f"| {rule.id} | {rule.name} | " + " | ".join(cells) + " |")
    cells = [f"{r['rows_with_violation']:,} ({r['percentage_rows_with_violation']:.2f}%)" for r in results]
    lines.append("| | **Rows with at least 1 violation** | " + " | ".join(cells) + " |")
    lines.append("| | Number of rows | " + " | ".join(f"{r['rows']:,}" for r in results) + " |")
    for key, name in [("mean", "mean"), ("median", "median"), ("max", "maximum")]:
        cells = [f"{r['spmse'][key]:.2f}" for r in results]
        lines.append(f"| | S_pMSE {name} (lower is better) | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def biggest_changes(base: dict, other: dict, top: int = 10) -> pd.DataFrame:
    """Column pairs whose S_pMSE increased most from ``base`` to ``other``."""
    a = base["_spmse_table"].rename(columns={"S_pMSE": base["label"]})
    b = other["_spmse_table"].rename(columns={"S_pMSE": other["label"]})
    merged = a.merge(b, on=["column1", "column2"])
    for col in (base["label"], other["label"]):
        merged[col] = merged[col].astype(float)
    merged["difference"] = merged[other["label"]] - merged[base["label"]]
    return merged.sort_values("difference", ascending=False).head(top).reset_index(drop=True)


def frame_to_markdown(df: pd.DataFrame) -> str:
    """A small Markdown table without extra dependencies."""
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for row in df.itertuples(index=False):
        cells = [f"{v:.3f}" if isinstance(v, float) else str(v) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def to_json(result: dict) -> dict:
    """The result without the full S_pMSE table, ready for json.dumps."""
    return {k: v for k, v in result.items() if not k.startswith("_")}
