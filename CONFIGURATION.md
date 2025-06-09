# Configuration and Settings

## `config.json`
`jgtcommon.readconfig()` searches for a configuration JSON with trading credentials. Order of lookup:

1. Path provided as argument or `config.json` in the current directory.
2. `$HOME/.jgt/config.json`.
3. `/etc/jgt/config.json`.
4. Environment variables:
   - `JGT_CONFIG_JSON_SECRET` – entire JSON string.
   - `JGT_CONFIG` – JSON string.
   - `JGT_CONFIG_PATH` – path to a JSON file.

Set `export_env=True` to export keys like `user_id` or `password` as environment variables. Use `demo=True` to replace credentials with `*_demo` values if present.

## `settings.json`
`jgtcommon.load_settings()` merges settings from multiple locations in the following order (later entries override earlier ones):

1. `/etc/jgt/settings.json` and environment variable `JGT_SETTINGS_SYSTEM`.
2. `$HOME/.jgt/settings.json` and environment variable `JGT_SETTINGS_USER`.
3. `.jgt/settings.json` within the current directory.
4. `.jgt/settings.yml`, `jgt.yml`, and `_config.yml` (YAML files).
5. Environment variables `JGT_SETTINGS` and `JGT_SETTINGS_PROCESS`.
6. A custom path supplied via the `-ls/--settings` CLI option.

The resulting dictionary is cached by `get_settings()` for repeated access.

Use `jgtset` to export settings to a `.env` file for shell sourcing.
