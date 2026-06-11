"""Data loading and validation helpers for OHLCV research datasets.

This module is intentionally generic. It demonstrates the data engineering
structure used by the framework without exposing proprietary signal logic.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_CANDLE_COLUMNS = ("time", "open", "high", "low", "close", "volume")


def load_candles(path: str | Path, symbol: str | None = None) -> pd.DataFrame:
    """Load candle data from CSV and return a normalized OHLCV DataFrame."""
    frame = pd.read_csv(path)
    if symbol is not None and "symbol" not in frame.columns:
        frame["symbol"] = symbol
    return normalize_candles(frame)


def normalize_candles(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize timestamps, numeric columns, sorting, and duplicate rows."""
    missing = [column for column in REQUIRED_CANDLE_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required candle columns: {missing}")

    output = frame.copy()
    output["time"] = pd.to_datetime(output["time"], utc=True).dt.tz_localize(None)

    for column in ("open", "high", "low", "close", "volume"):
        output[column] = pd.to_numeric(output[column], errors="coerce")

    if "symbol" in output.columns:
        sort_columns = ["symbol", "time"]
        dedupe_columns = ["symbol", "time"]
    else:
        sort_columns = ["time"]
        dedupe_columns = ["time"]

    output = output.dropna(subset=list(REQUIRED_CANDLE_COLUMNS))
    output = output.sort_values(sort_columns)
    output = output.drop_duplicates(dedupe_columns, keep="last")
    return output.reset_index(drop=True)


def validate_ohlcv(frame: pd.DataFrame) -> dict[str, int]:
    """Return basic data-quality counts for an OHLCV dataset."""
    candles = normalize_candles(frame)
    invalid_high = candles["high"] < candles[["open", "close", "low"]].max(axis=1)
    invalid_low = candles["low"] > candles[["open", "close", "high"]].min(axis=1)
    invalid_volume = candles["volume"] < 0

    return {
        "rows": int(len(candles)),
        "invalid_high_rows": int(invalid_high.sum()),
        "invalid_low_rows": int(invalid_low.sum()),
        "negative_volume_rows": int(invalid_volume.sum()),
        "duplicate_time_rows": int(candles.duplicated(["symbol", "time"]).sum())
        if "symbol" in candles.columns
        else int(candles.duplicated(["time"]).sum()),
    }


def resample_candles(frame: pd.DataFrame, interval: str) -> pd.DataFrame:
    """Resample single-symbol OHLCV data to a larger interval."""
    candles = normalize_candles(frame)
    if "symbol" in candles.columns and candles["symbol"].nunique() > 1:
        raise ValueError("resample_candles expects one symbol at a time")

    resampled = (
        candles.set_index("time")
        .resample(interval, label="left", closed="left")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
        .dropna()
        .reset_index()
    )
    if "symbol" in candles.columns:
        resampled["symbol"] = candles["symbol"].iloc[0]
    return normalize_candles(resampled)
