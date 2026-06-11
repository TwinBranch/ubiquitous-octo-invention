# System Architecture

This project is organized as a research and analytics framework for systematic crypto futures strategies. The public version documents the engineering architecture while omitting proprietary signal logic and production parameters.

## High-Level Flow

flowchart
    A[Market Data] --> B[OHLCV Normalization]
    B --> C[Signal/Event Interface]
    C --> D[Portfolio Admission]
    D --> E[Position Sizing]
    E --> F[Backtest Replay]
    F --> G[Analytics & Reports]


## 1. Market Data Layer

The data layer ingests high-frequency candle data from Binance and standardizes it into a consistent OHLCV schema. Each market is mapped to a defined timeframe and normalized before being passed into research or backtesting workflows.

Responsibilities:

- Load candle data from CSV or API outputs
- Normalize timestamps to UTC
- Standardize `open`, `high`, `low`, `close`, and `volume` columns
- Sort and deduplicate time-series records
- Detect missing values and invalid candles
- Preserve a consistent schema across symbols

## 2. Signal/Event Interface

The signal layer converts market data into timestamped strategy events. In the private production system, this layer contains proprietary indicators and strategy rules. In this public version, it is represented as a stubbed interface.

Event examples:

- `entry_signal`
- `layer_signal`
- `exit_signal`
- `time_stop`
- `risk_exit`

Separating signals from portfolio execution makes the system easier to test, audit, and extend.

## 3. Portfolio Admission Layer

Candidate events are not automatically executed. They first pass through portfolio-level admission logic that evaluates current exposure, open positions, pending orders, and configured risk limits.

This layer answers questions such as:

- Is this symbol already active?
- How many symbols are currently open?
- How many entries are already assigned to this position?
- Would the new order exceed portfolio exposure limits?
- Should simultaneous candidates be ranked before selection?

## 4. Position Sizing Layer

Approved events are converted into target position sizes. The sizing layer separates account equity, leverage assumptions, per-entry allocation, and portfolio exposure constraints.

The public version includes generic sizing utilities. Exact production sizing rules are omitted.

## 5. Backtest Replay Engine

The backtest engine replays timestamped events through the same portfolio admission and sizing concepts used by the live framework. This allows research outputs to reflect portfolio constraints rather than isolated single-symbol performance.

Modeled behavior includes:

- Multi-asset event ordering
- Max concurrent symbols
- Max entries per symbol
- Position-level returns
- Portfolio equity updates
- Drawdown tracking
- Adverse excursion diagnostics

## 6. Reporting Layer

The reporting layer converts raw backtest records into analyst-friendly outputs.

Typical outputs:

- Trade log
- Daily equity curve
- Monthly returns
- Symbol attribution
- Drawdown history
- Profit factor
- Sharpe and Sortino ratios
- Return distribution charts

## 7. State And Auditability

The production-oriented design uses durable records for live state and event logs. This allows the system to recover after interruption and makes execution behavior auditable.

Tracked state includes:

- Active positions
- Pending orders
- Processed candle timestamps
- Execution responses
- Error messages
- Account snapshots

This reflects database administration concepts such as durable state, reproducible records, and structured logs.
