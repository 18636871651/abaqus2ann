"""Minimal tabular-data validation example for ANN workflows."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ("strain", "strain_rate", "temperature", "stress")
FEATURE_COLUMNS = ("strain", "log_strain_rate", "temperature")
TARGET_COLUMN = "stress"


def load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def validate_columns(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def build_features(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    validate_columns(frame)
    clean = frame.loc[:, REQUIRED_COLUMNS].copy()
    clean = clean.apply(pd.to_numeric, errors="coerce").dropna()
    clean = clean[clean["strain_rate"] > 0]
    clean["log_strain_rate"] = np.log(clean["strain_rate"])
    return clean.loc[:, FEATURE_COLUMNS], clean[TARGET_COLUMN]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a tabular constitutive-model dataset.")
    parser.add_argument("data_path", type=Path)
    args = parser.parse_args()

    frame = load_table(args.data_path)
    features, target = build_features(frame)
    print(f"features: {features.shape[0]} rows x {features.shape[1]} columns")
    print(f"target: {target.shape[0]} rows")


if __name__ == "__main__":
    main()
