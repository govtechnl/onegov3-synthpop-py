"""Business rules for the OneGov #3 synthpop.py challenge (homicide dataset).

Each rule is a function that takes a DataFrame and returns a boolean Series:
``True`` marks a row that VIOLATES the rule. The logic mirrors the checks in
``notebooks/BusinessRules.ipynb`` by DUO's Team Synthetische Data, including how
missing values are treated. The rules were made up by DUO for this hackathon:
they do not describe reality.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pandas as pd

# Column names, exactly as in data/Synthetic_Homicide.csv
URBAN = "Urban vs rural"
TIME_OF_DAY = "Time of day"
N_VICTIMS = "Single vs multiple homicide victims"
N_PERPS = "Single vs multiple homicide perpetrators"
CRIMESCENE = "Type of crimescene"
WEAPON = "Type of weapon used"
CONTEXT = "Context of homicide"
RELATIONSHIP = "Victim-perpetrator relationship"
SOLVED = "Solved vs unsolved homicide"
GENDER_VICTIM = "Gender of victim"
GENDER_PERP = "Gender of main perpetrator"
AGE_VICTIM = "Age of victim"
AGE_PERP = "Age of main perpetrator"
AGE_DIFF = "Age difference"
EVIDENCE = "Main evidence type"
BIRTHCOUNTRY_VICTIM = "Birthcountry of victim"
BIRTHCITY_PERP = "Birthcity of main perpetrator"
BIRTHCOUNTRY_PERP = "Birthcountry of main perpetrator"
DATE_CRIME = "Date of current crime"
DATE_PREVIOUS = "Date of previous crime main perpetrator"
DATE_RELEASE = "Date of release from current crime main perpetrator"
SENTENCE = "Years prison sentence main perpetrator"

# All columns in the order of the CSV. This is also synthpop-py's default
# synthesis order (column_order=None).
COLUMNS = [
    URBAN, TIME_OF_DAY, N_VICTIMS, N_PERPS, CRIMESCENE, WEAPON, CONTEXT,
    RELATIONSHIP, SOLVED, GENDER_VICTIM, GENDER_PERP, AGE_VICTIM, AGE_PERP,
    AGE_DIFF, EVIDENCE, BIRTHCOUNTRY_VICTIM, BIRTHCITY_PERP, BIRTHCOUNTRY_PERP,
    DATE_CRIME, DATE_PREVIOUS, DATE_RELEASE, SENTENCE,
]

# Which birth cities are valid for which birth country (from DUO's notebook).
# Some city names occur in more than one country on purpose: Harlingen, Napels,
# Leuven, Zurich, Spitsbergen, Deurne, Wezel, Bristol, London, Paris, Barcelona.
CITY_MAPPING: dict[str, set[str]] = {
    "Netherlands": {
        "Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven",
        "Groningen", "Tilburg", "Almere", "Breda", "Nijmegen",
        "Harlingen", "Napels", "Leuven", "Zurich", "Spitsbergen",
        "Deurne", "Wezel",
    },
    "Other non-European": {
        "New York", "Tokyo", "Dubai", "Sydney", "Cape Town",
        "Hong Kong", "Bangkok", "Kuala Lumpur", "Jakarta", "Lagos",
        "Harlingen", "Bristol", "London", "Paris", "Napels", "Barcelona",
    },
    "Other Europe": {
        "Berlin", "Paris", "Madrid", "Rome", "Vienna",
        "Prague", "Brussels", "Warsaw", "Budapest", "Lisbon",
        "Athens", "Copenhagen", "Stockholm", "Oslo", "Helsinki",
        "Dublin", "Zurich", "Geneva", "Munich", "Hamburg",
        "Napels", "Leuven", "Spitsbergen", "Bristol", "London",
        "Barcelona", "Deurne", "Wezel",
    },
}

MENTALLY_DISTURBED = "Killing by mentally disturbed person (non-family)"
FAMILY_EXCEPTIONS = ["(Step)Parent", "Other relative"]

# Rule 6.4: a confession requires all of these columns to be filled in.
CONFESSION_REQUIRED = [
    URBAN, TIME_OF_DAY, N_VICTIMS, N_PERPS, CRIMESCENE, WEAPON, CONTEXT,
    RELATIONSHIP, SOLVED, GENDER_VICTIM, GENDER_PERP, AGE_VICTIM, AGE_PERP,
    BIRTHCOUNTRY_VICTIM, BIRTHCOUNTRY_PERP, BIRTHCITY_PERP, AGE_DIFF, DATE_CRIME,
]


def _unsolved(df: pd.DataFrame) -> pd.Series:
    return df[SOLVED] == "Unsolved"


def rule_1_birthcity_in_birthcountry(df: pd.DataFrame) -> pd.Series:
    """1. The birth city of the main perpetrator lies in the birth country.

    A known city with an unknown country is a violation. An unknown city is
    always allowed.
    """
    city = df[BIRTHCITY_PERP]
    country = df[BIRTHCOUNTRY_PERP]
    city_known = city.notna()
    country_unknown = country.isna()

    def city_fits(c: object, k: object) -> bool:
        return c in CITY_MAPPING.get(k, set())

    fits = pd.Series(
        [city_fits(c, k) for c, k in zip(city, country, strict=True)], index=df.index
    )
    return (city_known & country_unknown) | (city_known & ~country_unknown & ~fits)


def rule_2_age_difference(df: pd.DataFrame) -> pd.Series:
    """2. Age difference = |age of main perpetrator - age of victim|.

    A filled-in age difference with a missing age also counts as a violation.
    """
    expected = (df[AGE_PERP] - df[AGE_VICTIM]).abs()
    return df[AGE_DIFF].notna() & (df[AGE_DIFF] != expected)


def rule_3_1_previous_before_current(df: pd.DataFrame) -> pd.Series:
    """3.1 The previous crime did not happen after the current crime."""
    return df[DATE_PREVIOUS] > df[DATE_CRIME]


def rule_3_2_release_after_current(df: pd.DataFrame) -> pd.Series:
    """3.2 Release for the current crime is not before the current crime."""
    return df[DATE_CRIME] > df[DATE_RELEASE]


def rule_4_max_sentence(df: pd.DataFrame) -> pd.Series:
    """4. Solved: at most 10 years. Unsolved: sentence is missing."""
    solved = df[SOLVED] == "Solved"
    return (solved & (df[SENTENCE] > 10.0)) | (_unsolved(df) & df[SENTENCE].notna())


def rule_5_minors_sentence(df: pd.DataFrame) -> pd.Series:
    """5. Under 18: at most 5 years, unless older than 12 and the
    relationship is (Step)Parent or Other relative."""
    age = df[AGE_PERP]
    exception = (age > 12.0) & df[RELATIONSHIP].isin(FAMILY_EXCEPTIONS)
    return (age < 18.0) & (df[SENTENCE] > 5.0) & ~exception


def rule_6_1_evidence_empty_if_unsolved(df: pd.DataFrame) -> pd.Series:
    """6.1 Main evidence type is empty if the case is unsolved."""
    return _unsolved(df) & df[EVIDENCE].notna()


def rule_6_2_bullets_only_with_firearm(df: pd.DataFrame) -> pd.Series:
    """6.2 'bullets' and 'ballistics' only if the weapon is a firearm."""
    in_scope = ~_unsolved(df) & df[EVIDENCE].isin(["bullets", "ballistics"])
    return in_scope & ~(df[WEAPON] == "Firearm")


def rule_6_3_no_confession_if_mentally_disturbed(df: pd.DataFrame) -> pd.Series:
    """6.3 No 'confession' by a mentally disturbed perpetrator (non-family)."""
    in_scope = ~_unsolved(df) & (df[CONTEXT] == MENTALLY_DISTURBED)
    return in_scope & (df[EVIDENCE] == "confession")


def rule_6_4_confession_requires_complete_record(df: pd.DataFrame) -> pd.Series:
    """6.4 'confession' only if all other columns are filled in (except the
    previous-crime date, release date and prison sentence)."""
    in_scope = ~_unsolved(df) & df[CONFESSION_REQUIRED].isna().any(axis=1)
    return in_scope & (df[EVIDENCE] == "confession")


@dataclass(frozen=True)
class Rule:
    id: str
    name: str
    columns: tuple[str, ...]
    check: Callable[[pd.DataFrame], pd.Series]


RULES: tuple[Rule, ...] = (
    Rule("1", "Geboorteplaats ligt in geboorteland",
         (BIRTHCITY_PERP, BIRTHCOUNTRY_PERP), rule_1_birthcity_in_birthcountry),
    Rule("2", "Leeftijdsverschil klopt met beide leeftijden",
         (AGE_DIFF, AGE_PERP, AGE_VICTIM), rule_2_age_difference),
    Rule("3.1", "Vorige misdaad niet na de huidige",
         (DATE_PREVIOUS, DATE_CRIME), rule_3_1_previous_before_current),
    Rule("3.2", "Vrijlating niet voor de huidige misdaad",
         (DATE_CRIME, DATE_RELEASE), rule_3_2_release_after_current),
    Rule("4", "Maximaal 10 jaar; leeg als onopgelost",
         (SENTENCE, SOLVED), rule_4_max_sentence),
    Rule("5", "Minderjarigen maximaal 5 jaar, met uitzondering",
         (AGE_PERP, SENTENCE, RELATIONSHIP), rule_5_minors_sentence),
    Rule("6.1", "Geen bewijs bij onopgeloste zaak",
         (EVIDENCE, SOLVED), rule_6_1_evidence_empty_if_unsolved),
    Rule("6.2", "Kogels en ballistiek alleen bij vuurwapen",
         (EVIDENCE, WEAPON), rule_6_2_bullets_only_with_firearm),
    Rule("6.3", "Geen bekentenis bij ontoerekeningsvatbaarheid",
         (EVIDENCE, CONTEXT), rule_6_3_no_confession_if_mentally_disturbed),
    Rule("6.4", "Bekentenis alleen bij volledig ingevuld record",
         (EVIDENCE, *CONFESSION_REQUIRED), rule_6_4_confession_requires_complete_record),
)

ALWAYS_ALLOWED_EVIDENCE = ("DNA", "fingerprints", "witnesses")  # rule 6.5


def violations(df: pd.DataFrame) -> dict[str, pd.Series]:
    """Return one boolean Series per rule id; True marks a violating row."""
    return {rule.id: rule.check(df).fillna(False).astype(bool) for rule in RULES}


def check_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Return a report with the number and share of violating rows per rule."""
    masks = violations(df)
    n = len(df)
    rows = []
    for rule in RULES:
        count = int(masks[rule.id].sum())
        rows.append({
            "regel": rule.id,
            "omschrijving": rule.name,
            "overtredingen": count,
            "percentage": round(100 * count / n, 2) if n else 0.0,
        })
    return pd.DataFrame(rows)


def any_violation(df: pd.DataFrame) -> pd.Series:
    """True for every row that violates at least one rule."""
    masks = violations(df)
    if not masks:
        return pd.Series(False, index=df.index)
    return pd.concat(masks, axis=1).any(axis=1)
