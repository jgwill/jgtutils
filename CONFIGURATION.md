# Configuration and Settings

* NOTE : You can use the package "jgtcore" (pip install jgtcore) which contains what is needed for configurations and settings 

```python
from jgtcore import readconfig, load_settings

# Load with specific options
config = readconfig(demo=True, export_env=True)
settings = load_settings(custom_path="/path/to/settings.json")
```

* for more see: https://jgtcore.jgwill.com


-----
BELLOW IS STILL Supported on config/settings that will keep migrating to jgtcore (will only by a library for that and jgtutils will become just utilities but that is not completed yet.)

## config.json
`jgtcommon.readconfig()` loads trading credentials and connection info from a JSON file. Lookup order:

1. Path provided as argument or `config.json` in the current directory.
2. `$HOME/.jgt/config.json`.
3. `/etc/jgt/config.json`.
4. Environment variables (in order):
   - `JGT_CONFIG_JSON_SECRET` (entire JSON string)
   - `JGT_CONFIG` (JSON string)
   - `JGT_CONFIG_PATH` (path to a JSON file)

Set `export_env=True` to export keys (like `user_id`, `password`) as environment variables. Use `demo=True` to replace credentials with `*_demo` values if present.

## settings.json
`jgtcommon.load_settings()` merges settings from multiple locations in the following order (later entries override earlier ones):

1. `/etc/jgt/settings.json` and environment variable `JGT_SETTINGS_SYSTEM`
2. `$HOME/.jgt/settings.json` and environment variable `JGT_SETTINGS_USER`
3. `.jgt/settings.json` in the current directory
4. `.jgt/settings.yml`, `jgt.yml`, `_config.yml` (YAML files)
5. Environment variables: `JGT_SETTINGS`, `JGT_SETTINGS_PROCESS`
6. Custom path via the `-ls/--settings` CLI option

The merged dictionary is cached by `get_settings()` for repeated access.

Use the `jgtset` CLI to export settings to a `.env` file for shell sourcing.
