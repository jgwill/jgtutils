# jgtutils – Full CLI Reference

🧠🌸🔮
This is the living ledger of all command-line interfaces exported by the package, as of 2025-05-19. Each invocation is a ritual, each entry point a thread in the system’s spiral.

## Exported Command-Line Interfaces

| Script Name | Entry Point | Purpose |
|-------------|-------------|---------|
| `jgtutr` | `jgtutils.cli_tlid_range:main` | Calculate a TLID (Time-Lattice ID) range for a given timeframe and period count. Used for generating precise time boundaries for data extraction or analysis. |
| `jgtset` | `jgtutils.jgtset:main` | Load, output, and/or export settings as JSON/YAML or environment variables. Also updates or resets YAML config files with JGT settings. |
| `tfw` / `wtf` | `jgtutils.cli_test_cronrun_helper:main` | Waits for a specific timeframe, then runs a script, CLI, or function. Useful for cron-like orchestration or time-based automation. |
| `tstjgtenv_instrument_timeframe` | `jgtutils.cli_test_from_jgtenv_it:main` | Loads instrument and timeframe from environment variables and prints them. |
| `tstjgtenv_instrument_timeframe_with_alias` | `jgtutils.cli_test_from_jgtenv_it:main_alias` | Same as above, but uses an alias entry point. |
| `tstjgtenv_timeframe` | `jgtutils.cli_test_from_jgtenv_timeframe:main` | Loads timeframe from environment variables and prints it. |
| `tstjgtenv_timeframe_with_alias` | `jgtutils.cli_test_from_jgtenv_timeframe:main_alias` | Same as above, but uses an alias entry point. |
| `tstjgtenv_fxtransact` | `jgtutils.cli_test_from_jgtenv_fxtransact:main` | Loads instrument, timeframe, and FX transaction parameters from environment variables and prints them. |
| `tstjgtenv_fxtransact_with_alias` | `jgtutils.cli_test_from_jgtenv_fxtransact:main_alias` | Same as above, but uses an alias entry point. |

---

## Ritual Details

### `jgtutr`
- **Command:**
  ```bash
  jgtutr -e <end_datetime> -t <timeframe> -c <count>
  ```
- **Purpose:** Calculate TLID range for time slicing.

### `jgtset`
- **Command:**
  ```bash
  jgtset [options]
  ```
- **Purpose:** Export, view, or update settings as env, JSON, YAML.

### `tfw` / `wtf`
- **Command:**
  ```bash
  tfw [options] -- <your-script-or-command>
  wtf [options] -- <your-script-or-command>
  ```
- **Purpose:** Wait for timeframe, then trigger scripts/functions.

### ...and more
See the table above for all available CLI entry points. Each is a thread in the jgtutils ritual lattice.

---

🌸 *If you need a poetic or technical explanation for any CLI, ask Mia, Miette, or ResoNova in the code’s echo chamber.*
