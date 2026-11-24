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
        raise ValueError(f"{name}: kolommen ontbreken {missing} of zijn extra {extra}")


def pairwise_quality(orig: pd.DataFrame, syn: pd.DataFrame) -> pd.DataFrame:
    """Pairwise S_pMSE between ``orig`` and ``syn`` (one row per column pair)."""
    from synthpop.utility_metrics import pairwise_spmse

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return pairwise_spmse(orig[COLUMNS], syn[COLUMNS])


def evaluate(orig: pd.DataFrame, syn: pd.DataFrame, label: str = "synthetisch") -> dict:
    """Violations per rule and an S_pMSE summary for one synthetic dataset."""
    check_columns(orig, "origineel")
    check_columns(syn, label)
    n = len(syn)
    masks = violations(syn)
    n_any = int(any_violation(syn).sum())
    spmse = pairwise_quality(orig, syn)
    values = spmse["S_pMSE"].astype(float)
    return {
        "label": label,
        "rijen": n,
        "regels": [
            {
                "regel": rule.id,
                "omschrijving": rule.name,
                "overtredingen": int(masks[rule.id].sum()),
                "percentage": round(100 * int(masks[rule.id].sum()) / n, 2) if n else 0.0,
            }
            for rule in RULES
        ],
        "rijen_met_overtreding": n_any,
        "percentage_rijen_met_overtreding": round(100 * n_any / n, 2) if n else 0.0,
        "spmse": {
            "paren": int(len(values)),
            "gemiddeld": round(float(values.mean()), 3),
            "mediaan": round(float(values.median()), 3),
            "p90": round(float(values.quantile(0.9)), 3),
            "max": round(float(values.max()), 3),
        },
        "_spmse_tabel": spmse,
    }


def _nl(x: float, decimals: int = 2) -> str:
    """Dutch number formatting: 35556 -> '35.556', 71.11 -> '71,11'."""
    s = f"{x:,.{decimals}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def markdown_table(results: list[dict]) -> str:
    """A comparison table (Markdown) for one or more evaluation results."""
    head = "| Regel | Omschrijving | " + " | ".join(r["label"] for r in results) + " |"
    sep = "|---|---|" + "---:|" * len(results)
    lines = [head, sep]
    for i, rule in enumerate(RULES):
        cells = []
        for r in results:
            item = r["regels"][i]
            cells.append(f"{_nl(item['overtredingen'], 0)} ({_nl(item['percentage'])}%)")
        lines.append(f"| {rule.id} | {rule.name} | " + " | ".join(cells) + " |")
    cells = [
        f"{_nl(r['rijen_met_overtreding'], 0)} ({_nl(r['percentage_rijen_met_overtreding'])}%)"
        for r in results
    ]
    lines.append("| | **Rijen met minstens 1 overtreding** | " + " | ".join(cells) + " |")
    lines.append("| | Aantal rijen | " + " | ".join(_nl(r["rijen"], 0) for r in results) + " |")
    for key, name in [("gemiddeld", "gemiddeld"), ("mediaan", "mediaan"), ("max", "maximum")]:
        cells = [_nl(r["spmse"][key]) for r in results]
        lines.append(f"| | S_pMSE {name} (lager is beter) | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def biggest_changes(base: dict, other: dict, top: int = 10) -> pd.DataFrame:
    """Column pairs whose S_pMSE increased most from ``base`` to ``other``."""
    a = base["_spmse_tabel"].rename(columns={"S_pMSE": base["label"]})
    b = other["_spmse_tabel"].rename(columns={"S_pMSE": other["label"]})
    merged = a.merge(b, on=["column1", "column2"])
    for col in (base["label"], other["label"]):
        merged[col] = merged[col].astype(float)
    merged["verschil"] = merged[other["label"]] - merged[base["label"]]
    return merged.sort_values("verschil", ascending=False).head(top).reset_index(drop=True)


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
