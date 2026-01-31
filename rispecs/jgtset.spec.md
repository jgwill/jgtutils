# jgtset (Settings Manager) Specification

> Export and Manage JGT Settings Across Formats

**Specification Version**: 1.0  
**Module**: `jgtutils/jgtset.py`  
**CLI Command**: `jgtset`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Exported settings in various formats (env vars, JSON, YAML) and synchronized configuration files.

**Achievement Indicator**: Running `jgtset -E` produces:
- Settings exported to `~/.jgt/env.sh`
- Ready for `source ~/.jgt/env.sh` in bash scripts

**Value Proposition**: Bridge JGT settings across shell environments, YAML config files, and programmatic access.

---

## Structural Tension

**Current Reality**: Settings live in `~/.jgt/settings.json` but need to be accessible in bash, YAML configs, and environment.

**Desired State**: Settings synchronized across all required formats.

**Natural Progression**: Load settings → Filter by keys → Format output → Export/update target.

---

## CLI Interface

```python
def main():
    """
    JGT Settings Export CLI.
    
    Arguments:
        -E, --export-env: Export settings as environment variables
        -K, --keys: Export only specified keys
        -J, --json: Print as JSON
        -Y, --yaml: Print as YAML
        -S, --silent: Silent output
        -V, --view: View settings list
        -O, --output: Specify output env file path
        -U, --update: Update existing YAML file with jgt settings
        -R, --reset-jgt-config: Reset YAML file's jgt section
        -ls, --settings: Load from specific settings file
    
    Examples:
        # Export all settings to env file
        jgtset -E
        
        # Export specific keys only
        jgtset -E -K instruments timeframes
        
        # Print as JSON
        jgtset -J
        
        # Print as YAML
        jgtset -Y
        
        # Update Jekyll _config.yml with jgt settings
        jgtset -U _config.yml jgt
        
        # View available settings keys
        jgtset -V
        
        # Export to custom file
        jgtset -E -O /tmp/my_env.sh
    """
```

---

## Core Functions

### Settings Loading

```python
def _load_settings(custom_path: str = None) -> dict:
    """
    Load settings from hierarchy:
        1. /etc/jgt/settings.json (system)
        2. ~/.jgt/settings.json (user)
        3. .jgt/settings.json (project)
        4. custom_path if provided
    
    Later files override earlier ones.
    """
    return jgtcommon.get_settings(custom_path=custom_path)
```

### Environment Export

```python
def export_keys_to_environ(
    _settings: dict = None,
    keys: List[str] = None,
    quiet: bool = True,
    env_file: str = None,
    custom_path: str = None
) -> None:
    """
    Export settings to environment file.
    
    Algorithm:
        1. Initialize env file with header
        2. Filter settings by keys if specified
        3. For each key-value pair:
           - Skip excluded keys (credentials, etc.)
           - Format lists as comma-separated quoted strings
           - Format bools as lowercase
           - Handle nested dicts recursively
           - Write to env file
    
    Output format:
        KEY=value
        LIST_KEY="item1,item2,item3"
        BOOL_KEY=true
    """
```

### JSON/YAML Output

```python
def dump_as_json_output(
    _settings: dict = None,
    keys: List[str] = None,
    custom_path: str = None
) -> str:
    """Return settings as formatted JSON string."""

def dump_as_yaml_output(
    _settings: dict = None,
    keys: List[str] = None,
    custom_path: str = None
) -> str:
    """Return settings as formatted YAML string."""
```

### YAML File Update

```python
def update_jgt_on_existing_yaml_file(
    target_filepath: str,
    _settings: dict = None,
    keys: List[str] = None,
    custom_path: str = None,
    target_key: str = 'jgt',
    add_on_only: bool = True
) -> dict:
    """
    Update existing YAML file with JGT settings.
    
    Algorithm:
        1. Load current YAML file
        2. Create backup (.bak)
        3. If add_on_only: merge only new keys
        4. Else: replace entire target_key section
        5. Remove excluded keys
        6. Save updated YAML
    
    Use cases:
        - Jekyll _config.yml integration
        - Docker compose settings
        - Ansible variable files
    """
```

---

## Settings Filtering

```python
# Excluded keys (never exported)
_JGTSET_EXCLUDED_ENV_EXPORT_KEYS = [
    "fx_user_id",
    "fx_password",
    "fx_url",
    "fx_connection",
    "fx_account"
]

# Optional included keys (from settings or env)
# jgtset_included: "instruments,timeframes,patterns"
# JGTSET_INCLUDED=instruments,timeframes,patterns
```

---

## List Formatting

```python
def __format_list_to_string(
    value: list,
    enquote: bool = True,
    single_quote: bool = False
) -> str:
    """
    Format list for shell export.
    
    Example:
        ["a", "b", "c"] -> '"a,b,c"'
        [1, 2, 3] -> '"1,2,3"'
    """
```

---

## Output File Location

```python
# Default env export path
~/.jgt/env.sh

# Structure
#!/bin/bash
# This file is generated by JGTSettingsCLI (jgtset)
instruments="EUR/USD,GBP/USD,USD/JPY"
timeframes="H1,H4,D1"
columns_to_remove="BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose"
```

---

## Integration Points

### jgtfxcon
- Read `instruments`, `timeframes` for batch operations
- Read `columns_to_remove` for data cleaning

### jgtml
- Read `patterns` for TTF column selection
- Read `ttf2run` for workflow configuration

### jgt-data-server
- Load settings at startup for API defaults

### jgt-code
- Access settings via MCP tools

---

## Dependencies

```python
import json
import ruamel.yaml  # Optional - graceful fallback
import dotenv
from jgtutils import jgtcommon
from jgtutils.jgtenv import get_dotenv_jgtset_export_path
```

---

## Quality Criteria

✅ **Multi-Format**: JSON, YAML, and env var export  
✅ **Selective Export**: Filter by key names  
✅ **YAML Integration**: Update existing config files  
✅ **Credential Protection**: Excluded keys never exported  
✅ **List Handling**: Proper shell-compatible formatting  
✅ **Hierarchical Loading**: System → User → Project override
