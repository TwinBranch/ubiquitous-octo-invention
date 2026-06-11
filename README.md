# Systematic Crypto Futures Research & Analytics Framework

A Python-based research and analytics framework for studying systematic crypto futures strategies. This project demonstrates skills in financial data engineering, time-series analysis, portfolio risk modeling, database-style data organization, automated reporting, and production-oriented workflow design.

Proprietary trading logic and production parameters are intentionally omitted. The public version focuses on the data pipeline, analytics architecture, portfolio controls, and reporting workflow.

## Project Overview

This framework was built to support the full lifecycle of quantitative strategy research:

- Ingest and normalize high-frequency market data
- Organize multi-asset time-series datasets
- Generate and validate strategy events
- Apply portfolio-level capital and risk constraints
- Backtest strategy behavior across historical regimes
- Analyze returns, drawdowns, adverse excursion, and trade distributions
- Produce structured CSV outputs and visual performance reports
- Maintain persistent live-state records for auditability and recovery

The goal of this repository is to showcase the analytical and data infrastructure behind a systematic trading research process.

## System Architecture

### 1. Market Data Pipeline

The system collects, cleans, and standardizes OHLCV market data across multiple crypto futures markets. Each asset is mapped to a defined timeframe and stored in a consistent schema for downstream research.

Core responsibilities:

- Historical candle ingestion
- Timestamp normalization
- OHLCV schema standardization
- Multi-asset dataset organization
- Missing-data and gap checks
- Strategy-timeframe alignment

### 2. Signal & Event Processing

The private production system generates strategy events from market data. In this public version, proprietary signal logic is removed or stubbed, while the event-processing structure remains documented.

The event layer is designed to support:

- Multi-symbol signal generation
- Timestamped trade events
- Entry and exit classification
- Event replay for backtesting
- Separation between signal generation and portfolio execution logic

### 3. Portfolio Risk & Capital Allocation

Candidate trade events are evaluated through portfolio-level rules before being included in a backtest or live execution workflow.

This layer models:

- Maximum concurrent assets
- Maximum entries per asset
- Total portfolio exposure
- Per-position sizing
- Leverage-aware capital usage
- Portfolio-level adverse excursion
- Drawdown and recovery behavior

### 4. Backtesting Engine

The backtesting workflow replays historical trade events through the same portfolio and sizing rules used by the execution framework.

Outputs include:

- Trade-level records
- Position-level returns
- Portfolio equity curve
- Monthly return table
- Drawdown history
- Profit factor
- Sharpe and Sortino ratios
- Win/loss distributions
- Adverse excursion analysis

### 5. Reporting & Analytics

The framework produces structured outputs suitable for analysis in Python, spreadsheets, dashboards, or databases.

Generated artifacts include:

- CSV trade logs
- Daily equity tables
- Monthly return summaries
- Symbol-level attribution
- Drawdown reports
- Return distribution charts
- Portfolio risk visualizations
- Performance summary tables

### 6. State Management & Auditability

The live-oriented components persist execution state and event logs in structured files so the system can be audited and recovered after interruption.

Tracked state includes:

- Active positions
- Pending orders
- Processed candle timestamps
- Execution responses
- Error messages
- Account/equity snapshots

This design reflects database administration concepts such as durable records, recoverable state, structured logs, and reproducible data lineage.

## Skills Demonstrated

- Python data analysis
- Financial time-series processing
- Quantitative research workflow design
- Portfolio risk modeling
- Backtesting and simulation
- Data cleaning and validation
- CSV/JSONL-based data storage
- Structured logging
- Automated reporting
- Performance attribution
- Linux/VPS deployment workflow
- API integration
- State reconciliation and recovery

## Repository Scope

This public repository is designed as a portfolio project for finance, data analyst, and database-adjacent roles.

Included:

- System architecture documentation
- Data pipeline structure
- Backtesting/reporting workflow
- Portfolio risk-control design
- Example schemas and sanitized outputs
- Non-proprietary execution framework components

Excluded:

- Proprietary trading signals
- Exact production parameters
- API credentials
- Raw private account logs
- Full live trading configuration
- Sensitive trade-level alpha

## Disclaimer

This repository is for technical demonstration and research purposes only. It is not financial advice and does not include a complete production trading strategy.
