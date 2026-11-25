# Data card: Synthetic_Homicide.csv

| | |
|---|---|
| File | `Synthetic_Homicide.csv` (comma-separated, UTF-8, header row with column names) |
| Size | 1,291 rows (cases), 22 columns |
| Provided by | Team Synthetische Data, DUO, for OneGov #3 |
| Based on | Krüsselmann, K., Achterberg, J., Haas, M., Spruit, M. & Liem, M. (2024). *Synthetic Dutch Homicide Monitor* [Data set]. Leiden University/LUMC. [doi.org/10.5281/zenodo.13378063](https://doi.org/10.5281/zenodo.13378063) |
| Licence | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), with attribution as above |
| Background | [dutchhomicide.streamlit.app](https://dutchhomicide.streamlit.app/) |

## What is this data?

A synthetic version of the Dutch Homicide Monitor, about homicides in the Netherlands. It contains no real people or cases. A real dataset with this content may not be shared, so in the hackathon this synthetic set counts as the 'real' dataset. Teams create a new synthetic version of it that follows the business rules.

## What did DUO change?

For the hackathon, DUO added seven columns, following business rules they made up themselves:

- Birthcity of main perpetrator
- Age difference
- Main evidence type
- Date of current crime
- Date of previous crime main perpetrator
- Date of release from current crime main perpetrator
- Years prison sentence main perpetrator

DUO also changed 'Age of victim' and 'Age of main perpetrator' so that they contain an exact number, by random sampling within the original range.

**The business rules do not describe reality.** The dataset in this repository breaks no rule at all. See [docs/business-rules.md](../docs/business-rules.md).

## Columns

Descriptions by DUO (translated). Values are in English, exactly as in the source. An empty cell is an unknown value.

| Column | Description | Type | Empty |
|---|---|---|---:|
| Urban vs rural | Area in which the homicide was committed | categorical (2) | 2.5% |
| Time of day | Moment of the day at which the homicide was committed | categorical (4) | 32.7% |
| Single vs multiple homicide victims | One or more victims | categorical (2) | 0% |
| Single vs multiple homicide perpetrators | One or more suspects | categorical (2) | 10.9% |
| Type of crimescene | Environment in which the homicide was committed | categorical (5) | 3.3% |
| Type of weapon used | The weapon with which the homicide was committed | categorical (8) | 10.1% |
| Context of homicide | Background or context of the homicide | categorical (9) | 13.0% |
| Victim-perpetrator relationship | Relationship between the victim and the main perpetrator | categorical (9) | 31.3% |
| Solved vs unsolved homicide | Whether the homicide was solved | categorical (2) | 0% |
| Gender of victim | Gender of the victim | categorical (2) | 1.0% |
| Gender of main perpetrator | Gender of the main perpetrator | categorical (2) | 7.9% |
| Age of victim | Age of the victim | numeric (0 to 100) | 4.4% |
| Age of main perpetrator | Age of the main perpetrator | numeric (7 to 99) | 11.9% |
| Age difference | Age difference between victim and main perpetrator | numeric (0 to 86) | 15.8% |
| Main evidence type | Main evidence of the case | categorical (6) | 13.0% |
| Birthcountry of victim | Birth country of the victim | categorical (3) | 43.8% |
| Birthcity of main perpetrator | Birth city of the main perpetrator | categorical (47) | 55.5% |
| Birthcountry of main perpetrator | Birth country of the main perpetrator | categorical (3) | 44.2% |
| Date of current crime | Date of the homicide | Unix time in seconds (Nov 2021 to Nov 2026) | 0% |
| Date of previous crime main perpetrator | Date of the main perpetrator's previous crime | Unix time in seconds | 43.1% |
| Date of release from current crime main perpetrator | Release date for the current crime | Unix time in seconds | 29.5% |
| Years prison sentence main perpetrator | Length of the prison sentence in years | numeric (0.1 to 10) | 29.5% |

The number in brackets for categorical columns is the number of distinct values. Dates with empty values are stored as decimals in the CSV (for example `1865116800.0`); `pandas.to_datetime(column, unit="s")` turns them into dates.

## Good to know

- The column order in the file is also the default order in which synthpop-py synthesises. What that means for the rules is in [docs/business-rules.md](../docs/business-rules.md#column-order).
- Some labels in the file are truncated or end with a comma, such as `Afternoon (12-6` and `Hitting, kicking or other similar physical violence without weapon,`. Leave them as they are: the rules and tests use the values as they appear in the file.
- DUO deliberately chose birth cities that really exist, including names that exist both in the Netherlands and abroad, such as Harlingen, Zurich, Napels and Spitsbergen. Such a city can therefore go with more than one birth country. The valid combinations are in DUO's notebook and in `CITY_MAPPING` in [rules.py](../src/rulecheck/rules.py).
- The dataset is about homicides. Even though it is synthetic, handle it with care, also in examples, pitches and demos.
