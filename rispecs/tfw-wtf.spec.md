# tfw/wtf (Timeframe Scheduler) Specification

> Production Trading Automation - Wait and Execute on Timeframe

**Specification Version**: 1.0  
**Module**: `jgtutils/timeframe_scheduler.py`  
**CLI Commands**: `tfw`, `wtf` (aliases)  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Time-synchronized execution of scripts, CLIs, or functions aligned with trading timeframes.

**Achievement Indicator**: Running `tfw -t H1 -S /path/to/refresh.sh` produces:
- Process waits until H1 bar close (01:00, 02:00, etc.)
- Script executes at precise timeframe boundary
- Loop continues indefinitely until terminated

**Value Proposition**: Automate trading workflows to execute exactly when new candles close, ensuring fresh data and proper timing.

---

## Structural Tension

**Current Reality**: Need to run trading logic at specific timeframe intervals but cron lacks precision for varying DST and market schedules.

**Desired State**: Automated execution precisely at candle close for any supported timeframe.

**Natural Progression**: Parse args → Calculate trigger times → Wait loop → Execute action → Repeat.

---

## CLI Interface

```python
def main():
    """
    JGT Timeframe Scheduler (tfw/wtf).
    
    Arguments:
        -t, --timeframe: Target timeframe (m1, m5, m15, m30, H1, H4, D1, W1, M1) [required]
        -X, --exit: Exit when timeframe is reached (one-shot)
        -S, -B, --script-to-run: Bash script to execute at timeframe
        -C, --cli-to-run: CLI command to execute at timeframe
        -F, --function: Bash function to run (requires load.sh)
        -M, --message: Message to display when timeframe reached
        -I, --in-message: Message to display when wait starts
        -N, --no-output: Suppress all output
        -v, --verbose: Verbosity level
    
    Examples:
        # Wait for H1 then exit
        tfw -t H1 -X
        
        # Run script every m15
        tfw -t m15 -S /opt/trading/refresh.sh
        
        # Execute CLI on H4
        wtf -t H4 -C python trading_pipeline.py
        
        # Run bash function from load.sh
        tfw -t D1 -F daily_report
    """
```

---

## Core Algorithm

```python
def main():
    """
    Main scheduler loop.
    
    Flow:
        1. Parse arguments
        2. Validate timeframe from args or JGT_TIMEFRAME env
        3. Get trigger times for timeframe
        4. Calculate sleep duration (60s for >m1, 2s for m1)
        5. Print start message (unless -N)
        6. Infinite loop:
           a. Get current time
           b. If current_time in trigger_times:
              - If --exit: print message and exit
              - If --script: run script with timeframe, time as args
              - If --cli: run CLI command
              - Else: call refreshTF()
              - Adjust sleep for execution duration
           c. Sleep 1 second
    """
```

---

## Timeframe Trigger Calculation

```python
def get_times_by_timeframe_str(timeframe: str) -> List[str]:
    """
    Generate all trigger times for a timeframe.
    
    Returns:
        List of "HH:MM" (or "HH:MM:SS" for m1) strings
    """

def get_timeframes_times_by_minutes(minutes: int) -> List[str]:
    """
    Calculate trigger times by minute interval.
    
    For minutes >= 60: start at 01:00 (forex new day)
    For minutes < 60: start at 00:00
    For m1: includes :00 and :01 seconds (catches late triggers)
    
    Examples:
        H4: ["01:00", "05:00", "09:00", "13:00", "17:00", "21:00"]
        H1: ["01:00", "02:00", ..., "23:00"]
        m15: ["00:00", "00:15", "00:30", "00:45", "01:00", ...]
        m1: ["00:00:00", "00:00:01", "00:01:00", "00:01:01", ...]
    """

def get_timeframe_daily_ending_time() -> str:
    """
    Calculate D1/W1/MN trigger time based on DST.
    
    Returns:
        "22:00:00" during DST (March-November)
        "21:00:00" outside DST
    
    DST calculation:
        Start: Second Sunday in March
        End: First Sunday in November
    """
```

---

## Script Execution

```python
def _run_script_to_run(script_to_run: List[str]) -> None:
    """
    Execute script with context arguments.
    
    Command: bash {script_path} {timeframe} {current_time} {extra_args...}
    
    Example:
        bash /opt/trading/refresh.sh H4 13:00
    
    Script receives:
        $1 = timeframe
        $2 = trigger time
        $3+ = extra arguments from CLI
    """

def _run_function(
    function_to_run: str,
    load_script: str = "/opt/binscripts/load.sh"
) -> None:
    """
    Execute bash function with sourced environment.
    
    Load script search order:
        1. .jgt/load.sh (current dir)
        2. ../.jgt/load.sh (parent dir)
        3. ~/.jgt/load.sh (home)
        4. /opt/binscripts/load.sh (system)
    
    Command: bash -c ". {load_script} && {function} {timeframe} {time}"
    """
```

---

## JSONL Output

```python
def _print_app_message(
    timeframe: str,
    msg: str,
    state: str = None,
    use_short: bool = True
) -> None:
    """
    Print structured JSONL message.
    
    Format:
        {"message": "...", "timeframe": "H4", "time": "13:00", "state": "reached"}
    
    States:
        - started: Wait initiated
        - reached: Timeframe triggered
        - error: Execution failed
        - canceled: User interrupted
    """
```

---

## Error Handling

```python
# Exit codes
DOTJGTENV_TIMEFRAME_NOT_FOUND_EXIT_ERROR_CODE = 51
SUBPROCESS_RUN_ERROR_EXIT_ERROR_CODE = 52
BASH_FUNCTION_RUN_EXIT_ERROR_CODE = 53
BASH_LOADER_ERROR_EXIT_ERROR_CODE = 54

# Behavior
# - Script failures: log error, continue loop (unless exit_on_error)
# - CLI failures: log error, continue loop
# - Function failures: exit if exit_on_error=True
```

---

## Integration with jgtapp

```python
# jgtapp.py wrapper function
def w(
    timeframe: str,
    script_to_run: str = None,
    exit_on_timeframe: bool = False
) -> None:
    """
    Wrapper for tfw in jgtapp.
    
    Called by:
        - jgtapp w -t H4 -X
        - fxmvstopgator loop action
        - Trading campaign automation
    """
```

---

## Environment Variables

```python
# Load timeframe from env if not provided
JGT_TIMEFRAME = "H4"

# Custom load script location
JGT_LOAD_SCRIPT = "/path/to/load.sh"
```

---

## Dependencies

```python
import datetime
import time
import subprocess
from jgtutils import jgtcommon
from jgtutils.jgtclihelper import print_jsonl_message
import jgtwslhelper as wsl
```

---

## Quality Criteria

✅ **DST Aware**: Correct D1/W1 timing across seasons  
✅ **Multiple Actions**: Script, CLI, function, or exit  
✅ **Execution Timing**: Adjusts sleep for script duration  
✅ **Structured Output**: JSONL for log parsing  
✅ **Graceful Errors**: Continues on failures  
✅ **m1 Precision**: Catches late triggers with :01 variant
