# JGTUtils RISE Specifications

> Reverse-engineer → Intent-extract → Specify → Export

This directory contains RISE-compliant specifications for JGTUtils - the utility and CLI layer extending JGTCore with command-line tools and helpers.

## Quick Start

1. **Start Here**: [`app.specs.md`](./app.specs.md) - Master specification
2. **Constants**: [`constants.spec.md`](./constants.spec.md) - Column name constants

## Specification Map

| Spec File | CLI Command | Module | Status |
|-----------|-------------|--------|--------|
| [`app.specs.md`](./app.specs.md) | - | Master Overview | ✅ |
| [`constants.spec.md`](./constants.spec.md) | - | jgtconstants.py | ✅ |
| [`jgtset.spec.md`](./jgtset.spec.md) | `jgtset` | Settings export/sync | ✅ |
| [`jgtutr.spec.md`](./jgtutr.spec.md) | `jgtutr` | TLID range calculator | ✅ |
| [`tfw-wtf.spec.md`](./tfw-wtf.spec.md) | `tfw`, `wtf` | Timeframe scheduler | ✅ |
| [`add-pattern.spec.md`](./add-pattern.spec.md) | `jgt-add-pattern` | Pattern management | ✅ |

```
app.specs.md                    ← Master specification (start here)
├── constants.spec.md           ← Column name constants
├── jgtset.spec.md              ← Settings export (jgtset)
├── jgtutr.spec.md              ← TLID range calculation (jgtutr)
├── tfw-wtf.spec.md             ← Timeframe scheduling (tfw/wtf)
└── add-pattern.spec.md         ← Pattern management (jgt-add-pattern)
```

## RISE Framework Compliance

✅ **Desired Outcome Definition** - What users CREATE, not problems to solve  
✅ **Structural Tension** - Current reality vs desired state drives progression  
✅ **Natural Advancement** - Clear flow from current to desired  
✅ **Autonomous Specification** - Another LLM could implement from spec alone

## CLI Tools Summary

| Command | Purpose | Used By |
|---------|---------|---------|
| `jgtset` | Export settings to env/JSON/YAML | Shell scripts, CI/CD, Jekyll |
| `jgtutr` | Calculate TLID date ranges | jgtfxcli, backtesting |
| `tfw`/`wtf` | Wait for timeframe, execute | jgtapp, trading automation |
| `jgt-add-pattern` | Manage column patterns | ttfcli pattern selection |

## Integration Points

### jgtapp (jgtml)
- Uses `tfw` via `jgtapp w -t H4 -X`
- Uses patterns via `ttf` command

### jgtfxcon
- Uses TLID ranges for historical data queries

### jgt-data-server
- Loads settings at startup

### jgt-code
- Accesses settings via MCP

## Specification Version

- **Version**: 1.0
- **Framework**: RISE
- **Created**: 2026-01-31
