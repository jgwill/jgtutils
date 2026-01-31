# JGTUtils RISE Specifications

> Reverse-engineer → Intent-extract → Specify → Export

This directory contains RISE-compliant specifications for JGTUtils - the utility and CLI layer extending JGTCore with command-line tools and helpers.

## Quick Start

1. **Start Here**: [`app.specs.md`](./app.specs.md) - Master specification
2. **CLI Tools**: [`cli.spec.md`](./cli.spec.md) - Command-line utilities
3. **Common**: [`common.spec.md`](./common.spec.md) - Shared utilities

## Specification Map

```
app.specs.md                    ← Master specification (start here)
├── cli.spec.md                 ← CLI tools (jgtset, jgtutr, tfw)
├── common.spec.md              ← jgtcommon utilities
├── timeframe.spec.md           ← Timeframe scheduling
├── pov.spec.md                 ← Point-of-view calculations
└── environment.spec.md         ← Environment helpers
```

## RISE Framework Compliance

✅ **Desired Outcome Definition** - What users CREATE, not problems to solve  
✅ **Structural Tension** - Current reality vs desired state drives progression  
✅ **Natural Advancement** - Clear flow from current to desired  
✅ **Autonomous Specification** - Another LLM could implement from spec alone

## Key Concepts

### CLI Tools
- **jgtset** - Settings export/display
- **jgtutr** - TLID range calculation  
- **tfw/wtf** - Timeframe-based command scheduling

### Utility Modules
- **jgtcommon** - Core utilities
- **jgtpov** - Point-of-view helpers
- **jgtclihelper** - CLI argument parsing
- **timeframe_scheduler** - Timeframe-aware scheduling

## Specification Version

- **Version**: 1.0
- **Framework**: RISE
- **Created**: 2026-01-31
