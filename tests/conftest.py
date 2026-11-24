from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Synthetic_Homicide.csv"
SAMPLE = ROOT / "tests" / "fixtures" / "synthetic_sample.csv"
NOTEBOOK = ROOT / "notebooks" / "BusinessRules.ipynb"

# One record that satisfies every business rule. Tests change one value at a time.
VALID = {
    "Urban vs rural": "Urban",
    "Time of day": "Evening (6-12)",
    "Single vs multiple homicide victims": "Single",
    "Single vs multiple homicide perpetrators": "Single",
    "Type of crimescene": "Private home",
    "Type of weapon used": "Firearm",
    "Context of homicide": "Criminal milieu",
    "Victim-perpetrator relationship": "Partner",
    "Solved vs unsolved homicide": "Solved",
    "Gender of victim": "Male",
    "Gender of main perpetrator": "Male",
    "Age of victim": 30.0,
    "Age of main perpetrator": 40.0,
    "Age difference": 10.0,
    "Main evidence type": "DNA",
    "Birthcountry of victim": "Netherlands",
    "Birthcity of main perpetrator": "Utrecht",
    "Birthcountry of main perpetrator": "Netherlands",
    "Date of current crime": 1_700_000_000,
    "Date of previous crime main perpetrator": 1_600_000_000.0,
    "Date of release from current crime main perpetrator": 1_800_000_000.0,
    "Years prison sentence main perpetrator": 8.0,
}


def records(*changes: dict) -> pd.DataFrame:
    """A DataFrame with one row per dict of changes applied to VALID."""
    return pd.DataFrame([{**VALID, **c} for c in changes])


@pytest.fixture(scope="session")
def original() -> pd.DataFrame:
    return pd.read_csv(DATA)


@pytest.fixture(scope="session")
def synthetic_sample() -> pd.DataFrame:
    return pd.read_csv(SAMPLE)
