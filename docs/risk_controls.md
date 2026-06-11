# Risk Controls

The framework is designed around portfolio-level risk management. Individual signals are evaluated in the context of current positions, pending orders, account equity, and exposure constraints.

Proprietary production thresholds are omitted from this public version.

## Portfolio Admission Controls

Before a candidate event is accepted, the system can evaluate:

- Number of active symbols
- Number of active entries per symbol
- Total active entries across the portfolio
- Existing pending orders
- Current exposure by symbol
- Total portfolio notional exposure
- Available capital assumptions

This prevents the backtest from assuming unlimited capital or unlimited simultaneous fills.

## Position Sizing Controls

Sizing is modeled as a separate layer from signal generation.

Generic inputs:

- Account equity
- Leverage assumption
- Allocation percentage
- Entry price
- Existing exposure

Generic calculation:

available_notional = account_equity * leverage
target_notional = available_notional * allocation_pct
quantity = target_notional / entry_price


This structure allows sizing assumptions to be tested independently from strategy signal logic.

## Exposure Controls

The framework can enforce:

- Maximum concurrent symbols
- Maximum entries per symbol
- Maximum total entries
- Maximum notional exposure
- Optional per-symbol exposure limits
- Optional portfolio utilization limits

## Exit Controls

The framework supports multiple exit categories:

- Strategy exit
- Time-based exit
- Risk-based exit
- Full-position close
- Portfolio-level close condition

The production system separates entry modeling from exit modeling so each can be audited independently.

## Drawdown And Adverse Excursion

Risk reporting includes both closed-equity drawdown and mark-to-market adverse excursion.

Closed-equity drawdown answers:

How far did realized portfolio equity fall from its prior peak?


Portfolio-level adverse excursion answers:

What was the worst unrealized portfolio loss while positions were open?


Both measures are useful because a strategy can look profitable on closed trades while still experiencing large intratrade stress.

## State Recovery

The live-oriented design persists enough state to recover after interruption.

Tracked items may include:

- Active positions
- Pending orders
- Processed candle timestamps
- Execution responses
- Error messages
- Last known account equity

On restart, the system can reconcile local state with exchange-reported positions and orders. This reduces the risk of duplicate entries or lost position tracking.

## Audit Logs

Execution and research events are written in structured formats such as CSV or JSONL. This supports:

- Post-trade analysis
- Error review
- Reproducibility
- Debugging
- Compliance-style audit trails

## Risk Philosophy

The framework treats risk as a portfolio property, not just a single-trade property. The goal is to evaluate how signals interact when multiple assets trigger close together, how capital is consumed, and how open positions affect total account stress.
