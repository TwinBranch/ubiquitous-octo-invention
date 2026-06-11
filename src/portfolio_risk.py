"""Generic portfolio risk and sizing utilities.

The functions here are deliberately non-proprietary. They illustrate how a
portfolio-aware framework can reason about exposure, leverage, and admission
limits without disclosing production parameters.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioLimits:
    max_symbols: int
    max_entries_per_symbol: int
    max_total_entries: int
    max_notional_utilization: float = 1.0


@dataclass(frozen=True)
class PositionState:
    symbol: str
    entries: int
    notional: float


def available_notional(account_equity: float, leverage: float) -> float:
    """Calculate post-leverage notional capacity."""
    if account_equity < 0:
        raise ValueError("account_equity must be non-negative")
    if leverage <= 0:
        raise ValueError("leverage must be positive")
    return account_equity * leverage


def target_order_notional(account_equity: float, leverage: float, allocation_pct: float) -> float:
    """Convert percent of post-levered equity into target order notional."""
    if allocation_pct < 0:
        raise ValueError("allocation_pct must be non-negative")
    return available_notional(account_equity, leverage) * (allocation_pct / 100.0)


def target_quantity(account_equity: float, leverage: float, allocation_pct: float, price: float) -> float:
    """Calculate order quantity from account equity, leverage, allocation, and price."""
    if price <= 0:
        raise ValueError("price must be positive")
    return target_order_notional(account_equity, leverage, allocation_pct) / price


def current_exposure(positions: list[PositionState]) -> float:
    """Return total open notional exposure."""
    return sum(position.notional for position in positions)


def can_admit_symbol(symbol: str, positions: list[PositionState], limits: PortfolioLimits) -> bool:
    """Check whether a new symbol can be admitted to the portfolio."""
    active_symbols = {position.symbol for position in positions if position.entries > 0}
    return symbol in active_symbols or len(active_symbols) < limits.max_symbols


def can_add_entry(symbol: str, positions: list[PositionState], limits: PortfolioLimits) -> bool:
    """Check whether another entry can be added for a symbol."""
    total_entries = sum(position.entries for position in positions)
    symbol_entries = sum(position.entries for position in positions if position.symbol == symbol)

    if total_entries >= limits.max_total_entries:
        return False
    if symbol_entries >= limits.max_entries_per_symbol:
        return False
    return can_admit_symbol(symbol, positions, limits)


def utilization_after_order(
    positions: list[PositionState],
    new_order_notional: float,
    account_equity: float,
    leverage: float,
) -> float:
    """Return portfolio notional utilization after adding a hypothetical order."""
    capacity = available_notional(account_equity, leverage)
    if capacity == 0:
        return 0.0
    return (current_exposure(positions) + new_order_notional) / capacity


def can_place_order(
    symbol: str,
    positions: list[PositionState],
    limits: PortfolioLimits,
    new_order_notional: float,
    account_equity: float,
    leverage: float,
) -> bool:
    """Check entry-count and notional-utilization constraints."""
    if not can_add_entry(symbol, positions, limits):
        return False
    utilization = utilization_after_order(positions, new_order_notional, account_equity, leverage)
    return utilization <= limits.max_notional_utilization

