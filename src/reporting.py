"""Reporting helpers for sanitized backtest outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def add_drawdown(equity_curve: pd.DataFrame) -> pd.DataFrame:
    """Add drawdown percentage to an equity curve DataFrame."""
    frame = equity_curve.copy()
    frame["time"] = pd.to_datetime(frame["time"])
    frame = frame.sort_values("time")
    frame["equity_peak"] = frame["equity"].cummax()
    frame["drawdown_pct"] = (frame["equity"] / frame["equity_peak"] - 1.0) * 100.0
    return frame


def monthly_returns(equity_curve: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple month-by-month returns from an equity curve."""
    frame = add_drawdown(equity_curve)
    frame["month"] = frame["time"].dt.to_period("M").astype(str)

    rows = []
    for month, group in frame.groupby("month", sort=True):
        start_equity = float(group.iloc[0]["equity"])
        end_equity = float(group.iloc[-1]["equity"])
        return_pct = (end_equity / start_equity - 1.0) * 100.0 if start_equity else np.nan
        rows.append(
            {
                "month": month,
                "start_equity": start_equity,
                "end_equity": end_equity,
                "return_pct": return_pct,
                "max_drawdown_pct": float(group["drawdown_pct"].min()),
            }
        )
    return pd.DataFrame(rows)


def profit_factor(trades: pd.DataFrame, pnl_column: str = "realized_pnl") -> float:
    """Calculate gross-profit / gross-loss profit factor."""
    pnl = pd.to_numeric(trades[pnl_column], errors="coerce").fillna(0.0)
    gross_profit = pnl[pnl > 0].sum()
    gross_loss = abs(pnl[pnl < 0].sum())
    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0
    return float(gross_profit / gross_loss)


def plot_equity_curve(equity_curve: pd.DataFrame, output_path: str | Path) -> None:
    """Save an equity and drawdown chart."""
    frame = add_drawdown(equity_curve)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    axes[0].plot(frame["time"], frame["equity"], color="#1f77b4", linewidth=2)
    axes[0].set_title("Portfolio Equity")
    axes[0].set_ylabel("Equity")
    axes[0].grid(True, alpha=0.3)

    axes[1].fill_between(frame["time"], frame["drawdown_pct"], 0, color="#c0392b", alpha=0.25)
    axes[1].plot(frame["time"], frame["drawdown_pct"], color="#c0392b", linewidth=1.5)
    axes[1].set_title("Drawdown")
    axes[1].set_ylabel("Drawdown %")
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def write_report_tables(
    equity_curve: pd.DataFrame,
    trades: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    """Write common report tables to CSV."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    add_drawdown(equity_curve).to_csv(output_dir / "equity_curve.csv", index=False)
    monthly_returns(equity_curve).to_csv(output_dir / "monthly_returns.csv", index=False)
    trades.to_csv(output_dir / "trade_log.csv", index=False)
