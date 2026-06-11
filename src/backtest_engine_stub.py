"""Minimal portfolio backtest scaffold.

This file demonstrates event replay and portfolio accounting structure while
omitting proprietary signal generation and production parameters.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from portfolio_risk import PortfolioLimits, PositionState, can_place_order, target_order_notional


@dataclass(frozen=True)
class StrategyEvent:
    event_time: pd.Timestamp
    symbol: str
    event_type: str
    price: float
    allocation_pct: float = 0.0


def generate_signals(_candles: pd.DataFrame) -> list[StrategyEvent]:
    """Placeholder for proprietary signal generation.

    The production strategy logic is intentionally removed from the public
    repository. The rest of the framework can be reviewed without exposing
    alpha-generating rules.
    """
    raise NotImplementedError("Proprietary signal logic omitted from public repository.")


class PortfolioBacktester:
    """Simple event replay engine for sanitized strategy events."""

    def __init__(self, initial_equity: float, leverage: float, limits: PortfolioLimits) -> None:
        self.initial_equity = float(initial_equity)
        self.equity = float(initial_equity)
        self.leverage = float(leverage)
        self.limits = limits
        self.positions: dict[str, PositionState] = {}
        self.trades: list[dict[str, object]] = []
        self.equity_curve: list[dict[str, object]] = []

    def run(self, events: list[StrategyEvent]) -> dict[str, pd.DataFrame]:
        """Replay events in chronological order."""
        for event in sorted(events, key=lambda item: item.event_time):
            if event.event_type == "entry_signal":
                self._handle_entry(event)
            elif event.event_type in {"exit_signal", "time_stop", "risk_exit"}:
                self._handle_exit(event)
            self._record_equity(event.event_time)

        return {
            "trades": pd.DataFrame(self.trades),
            "equity_curve": pd.DataFrame(self.equity_curve),
        }

    def _handle_entry(self, event: StrategyEvent) -> None:
        order_notional = target_order_notional(self.equity, self.leverage, event.allocation_pct)
        existing = list(self.positions.values())

        if not can_place_order(
            event.symbol,
            existing,
            self.limits,
            order_notional,
            self.equity,
            self.leverage,
        ):
            return

        current = self.positions.get(event.symbol, PositionState(event.symbol, 0, 0.0))
        self.positions[event.symbol] = PositionState(
            symbol=event.symbol,
            entries=current.entries + 1,
            notional=current.notional + order_notional,
        )

    def _handle_exit(self, event: StrategyEvent) -> None:
        position = self.positions.pop(event.symbol, None)
        if position is None:
            return

        # Public stub: realized PnL is intentionally simplified. A production
        # engine would track entry prices, quantities, fees, and mark-to-market
        # state at the leg level.
        realized_pnl = 0.0
        self.equity += realized_pnl
        self.trades.append(
            {
                "symbol": event.symbol,
                "exit_time": event.event_time,
                "exit_type": event.event_type,
                "closed_entries": position.entries,
                "closed_notional": position.notional,
                "realized_pnl": realized_pnl,
            }
        )

    def _record_equity(self, timestamp: pd.Timestamp) -> None:
        active_entries = sum(position.entries for position in self.positions.values())
        self.equity_curve.append(
            {
                "time": timestamp,
                "equity": self.equity,
                "active_symbols": len(self.positions),
                "active_entries": active_entries,
            }
        )

