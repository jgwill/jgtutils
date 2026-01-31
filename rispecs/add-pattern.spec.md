# jgt-add-pattern (Pattern Manager) Specification

> Manage Column Patterns in User Settings

**Specification Version**: 1.0  
**Module**: `jgtutils/add_pattern_to_home_settings.py`  
**CLI Command**: `jgt-add-pattern`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Named column patterns stored in `~/.jgt/settings.json` for use by TTF and other data processing tools.

**Achievement Indicator**: Running `jgt-add-pattern --add-pattern mz --columns jaw teeth lips ao ac` produces:
- Pattern "mz" saved to settings
- Available for `ttfcli -pn mz`

**Value Proposition**: Define reusable column sets for cross-timeframe feature generation without repeating column lists.

---

## Structural Tension

**Current Reality**: User needs specific columns from higher timeframes but must specify them each time.

**Desired State**: Named patterns accessible across all CLI tools.

**Natural Progression**: Load settings → Add/Update/Remove pattern → Save settings.

---

## CLI Interface

```python
def main():
    """
    Manage patterns in home settings.
    
    Arguments (mutually exclusive):
        --add-pattern NAME: Name of pattern to add
        --list-patterns: List all patterns
        --remove-pattern NAME: Name of pattern to remove
    
    Additional arguments:
        --columns COL1 COL2 ...: Columns for pattern (required with --add-pattern)
        --force: Overwrite existing pattern
    
    Examples:
        # Add new pattern
        jgt-add-pattern --add-pattern mz --columns jaw teeth lips ao ac
        
        # List all patterns
        jgt-add-pattern --list-patterns
        
        # Remove pattern
        jgt-add-pattern --remove-pattern mz
        
        # Force overwrite existing
        jgt-add-pattern --add-pattern mz --columns jaw teeth lips --force
    """
```

---

## Core Functions

### Settings I/O

```python
def load_home_settings() -> Dict[str, Any]:
    """
    Load settings from ~/.jgt/settings.json.
    
    Returns empty structure if file doesn't exist:
        {"patterns": {}}
    """

def save_home_settings(settings: Dict[str, Any]) -> bool:
    """
    Save settings to ~/.jgt/settings.json.
    
    Creates ~/.jgt directory if needed.
    Returns True on success, False on failure.
    """
```

### Pattern Management

```python
def add_pattern_to_settings(
    pattern_name: str,
    columns: List[str],
    force: bool = False
) -> bool:
    """
    Add or update a pattern.
    
    Algorithm:
        1. Load settings
        2. If pattern exists and not force: return False
        3. Add pattern with columns list
        4. Save settings
    
    Storage format:
        {"patterns": {"mz": {"columns": ["jaw", "teeth", "lips", "ao", "ac"]}}}
    """

def list_patterns() -> None:
    """
    Print all patterns with their columns.
    
    Output:
        Patterns in home settings:
        ----------------------------------------
        mz: jaw, teeth, lips, ao, ac
        williams: ao, ac, bz, sz
    """

def remove_pattern_from_settings(pattern_name: str) -> bool:
    """
    Remove a pattern from settings.
    
    Returns True if removed, False if not found.
    """
```

---

## Settings Structure

```json
{
    "patterns": {
        "mz": {
            "columns": ["jaw", "teeth", "lips", "ao", "ac"]
        },
        "williams": {
            "columns": ["ao", "ac", "aocolor", "accolor", "bz", "sz", "fh", "fl"]
        },
        "alligator": {
            "columns": ["jaw", "teeth", "lips", "bjaw", "bteeth", "blips", "tjaw", "tteeth", "tlips"]
        }
    }
}
```

---

## File Locations

```python
# Settings file
~/.jgt/settings.json

# Directory created if missing
~/.jgt/
```

---

## Integration with TTF

```python
# In ttfcli.py
# Pattern name is used to select columns:
ttfcli -i EUR/USD -t H4 -pn mz

# TTF loads pattern and uses columns for HTF features:
# jaw, teeth, lips, ao, ac from H4 → added to H1 data
```

---

## Default Patterns

```python
# Common patterns (suggested for setup)
patterns = {
    "mz": ["jaw", "teeth", "lips", "ao", "ac"],
    "ttf": ["jaw", "teeth", "lips", "ao", "ac", "aocolor", "accolor"],
    "alligator_all": ["jaw", "teeth", "lips", "bjaw", "bteeth", "blips", "tjaw", "tteeth", "tlips"],
    "signals": ["fdb", "fdbb", "fdbs", "zlcB", "zlcS", "bz", "sz"]
}
```

---

## Dependencies

```python
import argparse
import json
import os
import sys
from typing import List, Dict, Any
from jgtutils import jgtcommon
```

---

## Quality Criteria

✅ **CRUD Operations**: Add, list, remove patterns  
✅ **Force Overwrite**: Prevent accidental overwrites  
✅ **Home Directory**: User-level persistence  
✅ **Auto Directory**: Creates ~/.jgt if needed  
✅ **Clean Output**: Formatted pattern list
