import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import CSV_PATH
from src.transform import load_csv, transform_dataframe, quality
from src.validators import EXPECTED_COLUMNS, validate_columns


def test_raw_columns_no_missing_expected():
    df = load_csv(CSV_PATH)
    check = validate_columns(df)
    assert check["missing"] == [], f"Colonnes manquantes: {check['missing']}"


def test_transform_preserves_expected_columns():
    df_raw = load_csv(CSV_PATH)
    df = transform_dataframe(df_raw)

    for col in EXPECTED_COLUMNS:
        assert col in df.columns, f"Colonne manquante après transform: {col}"


def test_quality_after_transform_has_no_invalid_rules():
    df_raw = load_csv(CSV_PATH)
    df = transform_dataframe(df_raw)
    q = quality(df)

    invalid = q["invalid_rules"]
    for rule, count in invalid.items():
        assert count == 0, f"Règle qualité invalide après transform: {rule}={count}"


def test_quality_after_transform_not_worse_than_before():
    df_raw = load_csv(CSV_PATH)
    q_before = quality(df_raw)

    df = transform_dataframe(df_raw)
    q_after = quality(df)

    assert q_after["duplicate_rows"] <= q_before["duplicate_rows"]

    for rule, before_count in q_before["invalid_rules"].items():
        after_count = q_after["invalid_rules"][rule]
        assert after_count <= before_count
