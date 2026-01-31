# jgtutils Constants Specification

> Column Names and System-Wide Constants

**Specification Version**: 1.0  
**Module**: `jgtutils/jgtconstants.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Consistent column naming across the entire JGT ecosystem, ensuring all packages speak the same language for data columns and indicator names.

**Achievement Indicator**: All packages import constants from jgtutils and use the same column names, preventing typos and mismatches in DataFrame operations.

**Value Proposition**: Single source of truth for column names, zone colors, and configuration defaults.

---

## Price Column Constants

```python
# Standard OHLCV
OPEN = "Open"
HIGH = "High"
LOW = "Low"
CLOSE = "Close"
VOLUME = "Volume"
DATE = "Date"
MEDIAN = "Median"
BAR_HEIGHT = "bar_height"

# Bid columns
BIDOPEN = "BidOpen"
BIDHIGH = "BidHigh"
BIDLOW = "BidLow"
BIDCLOSE = "BidClose"

# Ask columns
ASKOPEN = "AskOpen"
ASKHIGH = "AskHigh"
ASKLOW = "AskLow"
ASKCLOSE = "AskClose"
```

---

## Alligator Constants

### Regular Alligator (5-8-13)

```python
JAW = "jaw"      # 13-period SMMA, shift 8
TEETH = "teeth"  # 8-period SMMA, shift 5
LIPS = "lips"    # 5-period SMMA, shift 3
```

### Big Alligator (34-55-89)

```python
BJAW = "bjaw"
BTEETH = "bteeth"
BLIPS = "blips"

BJAW_PERIODS = 89
BTEETH_PERIODS = 55
BLIPS_PERIODS = 34
```

### Tide Alligator (144-233-377)

```python
TJAW = "tjaw"
TTEETH = "tteeth"
TLIPS = "tlips"

TJAW_PERIODS = 377
TTEETH_PERIODS = 233
TLIPS_PERIODS = 144
```

---

## Oscillator Constants

```python
# Awesome Oscillator
AO = "ao"
AOAZ = "aoaz"    # AO above zero
AOBZ = "aobz"    # AO below zero
AOCOLOR = "aocolor"

# Accelerator Oscillator
AC = "ac"
ACCOLOR = "accolor"

# Zero Line Cross
ZLC = "zlc"
ZLCB = "zlcb"    # ZLC Buy
ZLCS = "zlcs"    # ZLC Sell

# Gator Oscillator
GL = "gl"        # Gator low
GH = "gh"        # Gator high
```

---

## Fractal Constants

```python
# Standard fractals
FH = "fh"        # Fractal high (5-bar)
FL = "fl"        # Fractal low (5-bar)

# Multi-period fractals
FH3 = "fh3"
FL3 = "fl3"
FH5 = "fh5"
FL5 = "fl5"
FH8 = "fh8"
FL8 = "fl8"
FH13 = "fh13"
FL13 = "fl13"
FH21 = "fh21"
FL21 = "fl21"
FH34 = "fh34"
FL34 = "fl34"
FH55 = "fh55"
FL55 = "fl55"
FH89 = "fh89"
FL89 = "fl89"
```

---

## Signal Constants

```python
# FDB signals
FDB = "fdb"        # Combined: 1 (buy), -1 (sell), 0 (none)
FDBB = "fdbb"      # FDB Buy
FDBS = "fdbs"      # FDB Sell

# Target for ML
FDB_TARGET = "target"

# AO Vector counts
VECTOR_AO_FDBS = "vaos"
VECTOR_AO_FDBB = "vaob"
VECTOR_AO_FDBS_COUNT = "vaosc"
VECTOR_AO_FDBB_COUNT = "vaobc"
VECTOR_AO_FDB_COUNT = "vaoc"
```

---

## Zone Constants

```python
# Zone signals
BZ = "bz"              # Buying zone
SZ = "sz"              # Selling zone
ZCOL = "zcol"          # Zone color
ZONE_SIGNAL = "zone_sig"

# Zone colors
buyingZoneColor = "green"
sellingZoneColor = "red"
nonTradingZoneColor = "gray"
```

---

## MFI Constants

```python
MFI = "mfi"            # Market Facilitation Index
MFI_SQUAT = "mfi_sq"   # Squat signal
MFI_GREEN = "mfi_g"    # Green signal
MFI_FADE = "mfi_f"     # Fade signal
MFI_FAKE = "mfi_k"     # Fake signal
MFI_SIG = "mfi_sig"    # Signal classification
```

---

## Peak Detection Constants

```python
PRICE_PEAK_ABOVE = "price_peak_above"
PRICE_PEAK_BELLOW = "price_peak_bellow"
AO_PEAK_ABOVE = "ao_peak_above"
AO_PEAK_BELLOW = "ao_peak_bellow"
```

---

## Mouth Water Constants

```python
MW_LIP_TOUCH_BUY = "mw_ltb"
MW_LIP_TOUCH_SELL = "mw_lts"
MW_TEETH_TOUCH_BUY = "mw_ttb"
MW_TEETH_TOUCH_SELL = "mw_tts"
```

---

## Configuration Defaults

```python
# Default bar counts
NB_BARS_BY_DEFAULT = 335
NB_BARS_BY_DEFAULT_IN_CDS = 300

# ML default columns
ML_DEFAULT_COLUMNS_TO_KEEP = [
    'High', 'Low', 'ao', 'ac',
    'jaw', 'teeth', 'lips',
    'fh', 'fl', 'fdbb', 'fdbs',
    'zlcb', 'zlcs', 'target',
    'vaosc', 'vaobc'
]

# Columns to remove from output
columns_to_remove = [
    'aofvalue', 'aofhighao', 'aoflowao',
    'aofhigh', 'aoflow', 'aocolor', 'accolor',
    'fdbbhigh', 'fdbblow', 'fdbshigh', 'fdbslow'
]
```

---

## Type Definitions

```python
# Column type hints
AOAZ_TYPE = int
AOBZ_TYPE = int
ZLC_TYPE = int
```

---

## Usage Pattern

```python
from jgtutils.jgtconstants import (
    HIGH, LOW, CLOSE, OPEN,
    JAW, TEETH, LIPS,
    BJAW, BTEETH, BLIPS,
    FDB, FDBB, FDBS,
    AO, AC, ZLC
)

# Use constants for column access
entry_price = df[HIGH].iloc[-1]
is_buy_signal = df[FDBB].iloc[-1] == 1
alligator_direction = df[LIPS].iloc[-1] < df[TEETH].iloc[-1]
```

---

## Quality Criteria

✅ **Single Source**: All column names defined once  
✅ **Type Safety**: Type hints for key columns  
✅ **Complete Coverage**: All Williams indicators included  
✅ **Consistent Naming**: Lowercase for indicator columns  
✅ **Backward Compatible**: Legacy aliases maintained
