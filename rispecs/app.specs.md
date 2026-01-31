# JGTUtils Application Specification

> Master specification for the JGT Utilities Package

**Specification Version**: 1.0  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: A comprehensive utility layer that provides CLI tools, configuration management, timeframe scheduling, and common helpers for all JGT trading operations.

**Achievement Indicator**: Users can manage settings, calculate time ranges, schedule time-based operations, and access common utilities through consistent CLI and library interfaces.

**Value Proposition**: Bridge the gap between core configuration (jgtcore) and higher-level trading packages with reusable utilities and CLI tools.

---

## Application Overview

JGTUtils is a Python package that:
1. Extends jgtcore with CLI tools for configuration management
2. Provides TLID (Time-Lattice ID) range calculations
3. Implements timeframe-aware scheduling (wait-for-timeframe)
4. Offers common utilities shared across JGT packages
5. Handles FX-specific calculations (POV, spreads)

---

## Structural Tension

**Current Reality**: Trading operations need time calculations, settings management, and scheduling that go beyond basic configuration.

**Desired State**: Unified utility layer provides CLI tools and library functions for all time-based, configuration, and helper operations.

**Natural Progression**: JGTUtils builds upon jgtcore, adding operational capabilities while remaining a dependency for higher-level packages.

---

## CLI Tools

### jgtset - Settings Management

**Purpose**: Load, output, and export settings as JSON/YAML or environment variables

```bash
# Display all settings as JSON
jgtset

# Export settings as .env for shell sourcing
jgtset --export-env > settings.env

# Update YAML config with JGT settings
jgtset --update-yaml jgt.yml
```

### jgtutr - TLID Range Calculator

**Purpose**: Calculate Time-Lattice ID ranges for data extraction

```bash
# Calculate TLID range for H1 timeframe, 500 bars ending now
jgtutr -e now -t H1 -c 500

# Calculate range for specific end datetime
jgtutr -e "2025-12-31 23:00" -t D1 -c 100
```

**Output**: Returns start and end TLID values for the requested range

### tfw / wtf - Wait-For-Timeframe

**Purpose**: Wait for a specific timeframe completion, then run a command

```bash
# Wait for next H1 bar, then run refresh
tfw -t H1 -- jgtcli --fresh

# Continuous mode: wait and run repeatedly
wtf -t H1 --loop -- cdscli --fresh
```

---

## Library API

### Configuration (via jgtcore)

```python
import jgtutils

# Simple configuration access
config = jgtutils.get_config()
demo_config = jgtutils.get_config(demo=True)

# Single setting access
instrument = jgtutils.get_setting('instrument', 'EUR/USD')
quotes_count = jgtutils.get_setting('quotes_count', 1000)

# One-call environment setup
config, settings = jgtutils.setup_environment(demo=True)
```

### Timeframe Utilities

```python
from jgtutils.timeframe_scheduler import (
    get_next_timeframe_boundary,
    wait_for_timeframe,
    TimeframePeriod
)

# Get next H1 bar boundary
next_h1 = get_next_timeframe_boundary('H1')

# Wait for next timeframe (blocking)
wait_for_timeframe('H1', callback=on_timeframe_complete)
```

### Common Utilities

```python
from jgtutils import jgtcommon

# Read configuration with options
config = jgtcommon.readconfig(demo=True, export_env=True)

# Load settings from custom path
settings = jgtcommon.load_settings(custom_path="/path/to/settings.json")

# Get all settings (cached)
all_settings = jgtcommon.get_settings()
```

### Point of View (POV)

```python
from jgtutils import jgtpov

# Calculate POV for instrument
pov = jgtpov.calculate_pov('EUR/USD', 'H4')
```

---

## Type Definitions

```python
from typing import Dict, Any, Optional, Callable
from datetime import datetime

# Timeframe types
Timeframe = str  # "m1", "m5", "m15", "m30", "H1", "H4", "D1", "W1", "M1"

# TLID is a timestamp string: "YYMMDDHHMI"
TLID = str

# Configuration types
Config = Dict[str, Any]
Settings = Dict[str, Any]

def get_next_timeframe_boundary(
    timeframe: Timeframe,
    from_time: Optional[datetime] = None
) -> datetime: ...

def wait_for_timeframe(
    timeframe: Timeframe,
    callback: Optional[Callable] = None,
    loop: bool = False
) -> None: ...

def calculate_tlid_range(
    end: datetime,
    timeframe: Timeframe,
    count: int
) -> tuple[TLID, TLID]: ...
```

---

## Creative Advancement Scenarios

### Scenario: Scheduled Data Refresh

**Desired Outcome**: Automatically refresh data when each H1 bar completes

**Current Reality**: User needs time-aware automation

**Natural Progression**:
1. User runs: `wtf -t H1 --loop -- cdscli --fresh`
2. tfw calculates next H1 boundary (e.g., 14:00:00)
3. Process sleeps until boundary + offset
4. Executes command: `cdscli --fresh`
5. Loops back to wait for next H1

**Resolution**: Set-and-forget data refresh aligned with market periods

### Scenario: Historical Data Range

**Desired Outcome**: Calculate exact TLID boundaries for backtesting

**Current Reality**: User needs 500 D1 bars ending 2025-12-31

**Natural Progression**:
1. User runs: `jgtutr -e "2025-12-31" -t D1 -c 500`
2. jgtutr parses timeframe and calculates periods
3. Start TLID: 2024-02-08 (500 D1 bars back)
4. End TLID: 2025-12-31
5. Output: `--tlid-start=2402080000 --tlid-end=2512310000`

**Resolution**: Precise time boundaries for data extraction

---

## Module Structure

```
jgtutils/
├── __init__.py           # Public API exports
├── jgtcommon.py          # Core utilities
├── jgtpov.py             # Point-of-view calculations
├── jgtclihelper.py       # CLI argument helpers
├── jgtcliconstants.py    # CLI constants
├── jgtconstants.py       # Shared constants
├── jgtenv.py             # Environment helpers
├── jgtset.py             # jgtset CLI
├── jgtos.py              # OS utilities
├── jgtwslhelper.py       # WSL compatibility
├── timeframe_scheduler.py # Timeframe scheduling
├── FXTransact.py         # FX transaction helpers
├── iprops.py             # Instrument properties
└── cli/                  # CLI entry points
```

---

## Integration with JGT Ecosystem

```
jgtcore
    ↓ provides configuration
jgtutils (this package)
    ↓ provides utilities + CLI
jgtapy (indicators)
jgtfxcon (broker connection)
jgtpy (data services)
jgtml (ML/analysis)
```

---

## Quality Criteria

✅ **CLI Consistency**: All tools follow same argument patterns  
✅ **Library Access**: Every CLI function available programmatically  
✅ **Timeframe Awareness**: Native understanding of trading timeframes  
✅ **Cross-Platform**: Works on Windows, Linux, WSL  
✅ **Demo Mode**: Inherits jgtcore demo/live switching
