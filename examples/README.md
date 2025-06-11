# Configuration Examples

This directory contains example configuration files for jgtutils.

## Files

### config.json
Main configuration file containing:
- Trading credentials (real and demo)
- Connection settings
- Data processing preferences
- Column filtering rules

**Location Search Order:**
1. Current directory: `config.json`
2. User home: `~/.jgt/config.json`
3. System wide: `/etc/jgt/config.json`
4. Environment variables: `JGT_CONFIG_JSON_SECRET`, `JGT_CONFIG`, `JGT_CONFIG_PATH`

### settings.json
Application settings containing:
- Timeframe definitions
- Pattern configurations
- Processing flags
- Output preferences

**Location Search Order:**
1. System: `/etc/jgt/settings.json`
2. User home: `~/.jgt/settings.json`
3. Current directory: `.jgt/settings.json`
4. YAML variants: `.jgt/settings.yml`, `jgt.yml`, `_config.yml`
5. Environment variables: `JGT_SETTINGS`, `JGT_SETTINGS_PROCESS`

## Configuration Schema

### config.json Structure
```json
{
  "user_id": "string",           // FXCM user ID
  "account": "string",           // Account number
  "password": "string",          // Password
  "user_id_demo": "string",      // Demo user ID
  "password_demo": "string",     // Demo password
  "account_demo": "string",      // Demo account
  "url": "string",              // FXCM connection URL
  "connection": "Real|Demo",     // Connection type
  "quotes_count": "number",      // Max quotes to fetch
  "pds_server_url": "string",    // PDS server URL
  "columns_to_remove": "array",  // Columns to filter out
  "keep_bid_ask": "boolean"      // Keep bid/ask data
}
```

### settings.json Structure
```json
{
  "quotes_count": "number",              // Max quotes
  "_timeframes": "string",               // Comma-separated timeframes
  "keepbidask": "boolean",               // Keep bid/ask flag
  "columns_to_remove": "array",          // Columns to remove
  "_selected_columns": "array",          // Columns to keep
  "mfi_flag": "boolean",                 // MFI indicator flag
  "balligator_flag": "boolean",          // Bill Alligator flag
  "talligator_flag": "boolean",          // Twin Alligator flag
  "ttf2run": "array",                    // Patterns to run
  "patterns": {                          // Pattern definitions
    "pattern_name": {
      "columns": "array"                 // Required columns
    }
  },
  "jgtset_excluded": "string"            // Keys excluded from export
}
```

## Usage Examples

### Load Configuration
```python
import jgtutils

# Load default config
config = jgtutils.get_config()

# Load demo config
demo_config = jgtutils.get_config(demo=True)

# Get specific config value
user_id = jgtutils.get_config_value('user_id')
```

### Load Settings
```python
import jgtutils

# Get all settings
settings = jgtutils.get_settings()

# Get specific setting
timeframes = jgtutils.get_setting('_timeframes', 'D1')
quotes_count = jgtutils.get_setting('quotes_count', 1000)
```

### Environment Setup
```python
import jgtutils

# One-call setup
config, settings = jgtutils.setup_environment(demo=True)
```