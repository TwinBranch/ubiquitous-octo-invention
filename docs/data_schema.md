# Data Schema

This document describes the core datasets used by the research and analytics framework. The schemas are designed for CSV, pandas DataFrames, or database tables.

## Candle Schema

| Column | Type | Description |
|---|---:|---|
| time | datetime | UTC candle timestamp |
| symbol | string | Market identifier |
| open | float | Open price |
| high | float | High price |
| low | float | Low price |
| close | float | Close price |
| volume | float | Traded volume |

Example:

csv
time,symbol,open,high,low,close,volume,2026-01-01 00:00:00,ASSET_A,100.00,101.20,99.80,100.75,125000


## Signal/Event Schema

| Column | Type | Description |
|---|---:|---|
| event_time | datetime | UTC timestamp for the event |
| symbol | string | Market identifier |
| event_type | string | Entry, layer, exit, or risk event |
| event_id | string | Event label or order layer identifier |
| reference_price | float | Price used by the event logic |
| metadata | string | Optional serialized metadata |

Example event types:

- `entry_signal`
- `layer_signal`
- `exit_signal`
- `time_stop`
- `risk_exit`

## Trade Log Schema

| Column | Type | Description |
|---|---:|---|
| trade_id | integer | Unique trade identifier |
| symbol | string | Sanitized market identifier |
| entry_time | datetime | Entry timestamp |
| exit_time | datetime | Exit timestamp |
| entry_price | float | Entry price |
| exit_price | float | Exit price |
| quantity | float | Position quantity |
| notional | float | Entry notional |
| return_pct | float | Trade return in percent |
| mae_pct | float | Maximum adverse excursion in percent |
| exit_reason | string | Exit category |

## Equity Curve Schema

| Column | Type | Description |
|---|---:|---|
| time | datetime | Timestamp of equity observation |
| equity | float | Portfolio equity |
| drawdown_pct | float | Drawdown from prior equity peak |
| active_symbols | integer | Count of open symbols |
| active_entries | integer | Count of open entries |

## Monthly Return Schema

| Column | Type | Description |
|---|---:|---|
| month | string | Month in `YYYY-MM` format |
| start_equity | float | Equity at month start |
| end_equity | float | Equity at month end |
| return_pct | float | Monthly return in percent |
| trades | integer | Number of closed trades |
| max_drawdown_pct | float | Worst drawdown during month |

## Symbol Attribution Schema

| Column | Type | Description |
|---|---:|---|
| symbol | string | Sanitized market identifier |
| trades | integer | Number of trades |
| win_rate_pct | float | Percent of winning trades |
| gross_profit | float | Sum of profitable trade PnL |
| gross_loss | float | Absolute value of losing trade PnL |
| profit_factor | float | Gross profit divided by gross loss |
| net_pnl | float | Net PnL contribution |

## Data Quality Checks

The framework is designed to support:

- Duplicate timestamp checks
- Missing candle checks
- Invalid OHLC checks
- Timezone normalization
- Symbol-to-timeframe mapping validation
- Event timestamp alignment
- Schema validation before reporting

