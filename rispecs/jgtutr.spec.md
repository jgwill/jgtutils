# jgtutr (TLID Range Calculator) Specification

> Timeline ID Range Calculator for Date-based Data Queries

**Specification Version**: 1.0  
**Module**: `jgtutils/cli_tlid_range.py`  
**CLI Command**: `jgtutr`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: TLID (Timeline ID) range strings for querying historical price data over specific date periods.

**Achievement Indicator**: Running `jgtutr -e 2026-01-31 -t H4 -c 100` produces:
- TLID range string for 100 H4 periods ending at given date
- Format suitable for passing to data query CLIs

**Value Proposition**: Automatically calculate date ranges for backtesting and historical data retrieval without manual date math.

---

## Structural Tension

**Current Reality**: User knows "last 100 H4 bars ending today" but needs specific date range.

**Desired State**: Precise TLID range string usable by other CLI tools.

**Natural Progression**: Parse args → Calculate period duration → Subtract from end date → Format output.

---

## CLI Interface

```python
def main():
    """
    Calculate TLID range for data queries.
    
    Arguments:
        -e: End datetime (ISO format or descriptive)
        -t: Timeframe (m1, m5, m15, m30, H1, H4, D1, W1, MN)
        -c: Number of periods/bars to include
    
    Examples:
        # Last 100 H4 bars
        jgtutr -e 2026-01-31 -t H4 -c 100
        
        # Last 500 daily bars
        jgtutr -e 2026-01-31 -t D1 -c 500
        
        # 1000 M15 bars ending at specific time
        jgtutr -e "2026-01-31T12:00" -t m15 -c 1000
    
    Output:
        TLID range string formatted for -tlid argument
    """
```

---

## Core Function

```python
from jgtpov import calculate_tlid_range as get_tlid_range

def main():
    # Parse arguments
    args = parser.parse_args()
    
    # Calculate TLID range
    result = get_tlid_range(args.e, args.t, args.c)
    
    # Print result
    print(result)
```

---

## TLID Range Format

```python
# Output format
"{start_tlid}_{end_tlid}"

# Example
"260101_260131"  # Jan 1-31, 2026

# Used in other CLIs
jgtfxcli -i EUR/USD -t H4 --tlidrange 260101_260131
```

---

## Timeframe Duration Mapping

| Timeframe | Minutes | Used For |
|-----------|---------|----------|
| m1 | 1 | High-frequency analysis |
| m5 | 5 | Short-term scalping |
| m15 | 15 | Intraday trading |
| m30 | 30 | Intraday swings |
| H1 | 60 | Day trading |
| H4 | 240 | Swing trading |
| D1 | 1440 | Position trading |
| W1 | 10080 | Long-term trends |
| MN | 43200 | Macro analysis |

---

## Integration Points

- **jgtfxcli**: Pass TLID range for historical data fetch
- **cdscli**: Generate signals for specific date range
- **ttfcli**: Process cross-TF features for period
- **jgtapp**: Used in backtesting workflows

---

## Dependencies

```python
from jgtpov import calculate_tlid_range
import argparse
```

---

## Quality Criteria

✅ **Timeframe Aware**: Correct period calculation per TF  
✅ **Flexible Dates**: Multiple input formats supported  
✅ **CLI Ready**: Output suitable for other tools  
✅ **Simple Interface**: Just 3 arguments
