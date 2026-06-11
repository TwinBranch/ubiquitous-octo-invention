# Backtest Methodology

The backtesting workflow is designed to evaluate strategy behavior at the portfolio level rather than treating each market as an isolated trade stream.

Proprietary signal rules are omitted from this public repository. The methodology below describes the non-proprietary replay and analytics framework.

## Objective

The backtester answers:

- What would happen if timestamped strategy events were replayed in chronological order?
- How do portfolio limits affect trade selection?
- How does leverage-aware sizing affect returns and drawdowns?
- What is the portfolio-level adverse excursion during open positions?
- How stable are returns across months and market regimes?

## Event Replay

Input events are sorted by timestamp and processed in chronological order. Each event is evaluated against current portfolio state before being accepted.

Event records generally include:

- Timestamp
- Symbol
- Event type
- Reference price
- Entry or exit identifier
- Optional sizing metadata

The replay engine maintains active positions, pending entries, realized PnL, equity history, and portfolio exposure.

## Portfolio Constraints

The backtest applies portfolio rules before accepting candidate events.

Examples:

- Maximum concurrent symbols
- Maximum entries per symbol
- Maximum total entries
- Position-level exposure limits
- Portfolio-level exposure limits
- Optional ranking of simultaneous candidates

This design avoids overstating performance by assuming every independent symbol signal could be traded without capital or exposure constraints.

## Position Sizing

Sizing is modeled separately from signal generation. The framework supports leverage-aware notional sizing and configurable per-entry allocation rules.

Generic sizing formula:

available_notional = account_equity * leverage
target_notional = available_notional * allocation_pct
quantity = target_notional / entry_price


Exact production sizing parameters are intentionally not included.

## Entry And Exit Modeling

The framework supports limit-style entries and market-style exits as separate concepts.

In research mode:

- Entry events can be modeled at a reference price or limit price
- Exit events close the active position or campaign
- Time-based exits can be evaluated from first fill time
- Adverse excursion can be computed using candle lows during the open interval

## Portfolio Equity

Equity is updated from realized trade outcomes and can also be marked to market during open positions.

Common outputs:

- Event-level equity
- Daily equity
- Monthly returns
- Drawdown curve
- Recovery duration
- Portfolio-level MAE

## Performance Metrics

The reporting workflow calculates:

- Total return
- Daily geometric mean return
- Monthly return distribution
- Win rate
- Profit factor
- Maximum drawdown
- Longest recovery period
- Sharpe ratio
- Sortino ratio
- Symbol-level attribution
- Return and drawdown distributions

## Validation Approach

The framework is designed to support validation checks such as:

- Comparing generated events against expected event logs
- Auditing candle coverage and timestamp alignment
- Checking for missing data
- Verifying portfolio exposure limits
- Stress testing simultaneous signals
- Testing sensitivity to sizing assumptions

The public repository includes simplified examples to demonstrate methodology without exposing proprietary strategy logic.
