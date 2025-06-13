# JGTUtils → JGTCore Migration & Refactoring Plan

## Executive Summary

This document outlines a comprehensive refactoring strategy to properly separate utilities from libraries in the jgtutils package, continuing the migration to jgtcore. The current codebase has mixed responsibilities and requires strategic restructuring to achieve clean separation of concerns.

## Current State Analysis

### Migration Status: Partially Complete ✅
- **jgtcore** already exists and contains core library functions
- **jgtutils** depends on `jgtcore>=0.1.0`
- Core functions are imported from jgtcore and re-exposed in jgtutils
- **Critical Issue**: Large monolithic files with mixed responsibilities

### Key Problems Identified 🚨
1. **jgtcommon.py** (2,327 lines) - Massive file with mixed CLI/library functionality
2. **Duplicate functionality** between jgtutils and jgtcore
3. **Unclear boundaries** between utilities and libraries
4. **Trading domain logic** scattered across utility modules

## Detailed Analysis

### ✅ Already Migrated to jgtcore
Core library functions successfully moved:
- Configuration management: `get_config`, `get_setting`, `setup_environment`
- Settings handling: `readconfig`, `load_settings`, `get_settings`
- Utility functions: `dt_from_last_week_as_string_fxformat`

### 🔧 Utilities (Should remain in jgtutils)

#### CLI Tools & Helpers
- `jgtclihelper.py` (44 lines) - JSON message formatting, signal handling
- `jgtcliconstants.py` (195 lines) - CLI argument constants and groups
- `cli_test_*.py` files - CLI testing utilities

#### OS & File System Utilities
- `jgtos.py` (325 lines) - File path utilities, data directory management
- `jgtfxhelper.py` (137 lines) - FX-specific file helpers  
- `jgtwslhelper.py` (172 lines) - WSL-specific utilities

#### Environment & Configuration Utilities
- `jgtenv.py` (105 lines) - Environment loading utilities
- `jgtset.py` (404 lines) - Configuration management utilities

#### POV (Point of View) Utilities
- `jgtpov.py` (304 lines) - Timeframe calculations and date handling

### 📚 Libraries (Should migrate to jgtcore)

#### Trading Domain Logic
- `FXTransact.py` (1,019 lines) - Core trading data structures and business logic
- Trading-specific constants from `jgtconstants.py`

#### Data Processing Libraries
- Column manipulation utilities
- Type conversion helpers (`coltypehelper.py`, `colconverthelper.py`)

### ⚠️ Critical Refactoring Needed

#### jgtcommon.py (2,327 lines) - **HIGHEST PRIORITY**
Mixed responsibilities that need separation:
- **CLI argument parsing** → Stay in jgtutils
- **Settings management** → Remove duplicates (already in jgtcore)
- **Configuration loading** → Remove duplicates (already in jgtcore)
- **Market timing functions** → Move to jgtcore
- **Date/time utilities** → Move to jgtcore

## 4-Phase Refactoring Strategy

### Phase 1: Split jgtcommon.py 🎯 **HIGH PRIORITY**

```
jgtcommon.py (2,327 lines) →
├── jgtcliarguments.py (CLI parsing utilities - stay in jgtutils)
├── jgtmarket.py (Market timing - move to jgtcore)
├── jgtdatetime.py (Date/time utilities - move to jgtcore)
└── Remove duplicates (already in jgtcore)
```

**Actions:**
1. Extract CLI argument parsing functions → `jgtutils/cli/arguments.py`
2. Extract market timing functions → `jgtcore/market/timing.py`
3. Extract date/time utilities → `jgtcore/datetime/utils.py`
4. Remove duplicate settings/config code
5. Update imports across codebase

### Phase 2: Migrate Trading Libraries to jgtcore

```
jgtutils/ → jgtcore/
├── FXTransact.py → jgtcore/trading/models.py
├── Trading constants → jgtcore/constants/trading.py
├── Market utilities → jgtcore/market/utils.py
└── Data processing → jgtcore/data/processing.py
```

**Actions:**
1. Move `FXTransact.py` to jgtcore trading module
2. Migrate trading-specific constants
3. Move data processing libraries
4. Update all import statements

### Phase 3: Clean Utilities Structure

```
jgtutils/ (utilities only)
├── cli/ (CLI tools and helpers)
│   ├── arguments.py
│   ├── helpers.py
│   └── constants.py
├── os/ (OS and file system utilities)
│   ├── paths.py
│   ├── fx_helpers.py
│   └── wsl_helpers.py
├── env/ (Environment utilities)
│   ├── loading.py
│   └── management.py
└── pov/ (POV utilities)
    └── calculations.py
```

**Actions:**
1. Reorganize utilities into logical modules
2. Clean up imports and dependencies
3. Remove any remaining library code
4. Update CLI entry points

### Phase 4: Update Dependencies and Imports

**Actions:**
1. Update jgtcore with new library modules
2. Update jgtutils imports to use jgtcore for library functions
3. Remove duplicate code completely
4. Update CLI scripts to use proper separation
5. Update documentation and examples

## Target Architecture

### jgtcore (Libraries) 📚
```
jgtcore/
├── __init__.py (core API)
├── config/
│   ├── __init__.py
│   ├── loader.py
│   └── settings.py
├── trading/
│   ├── __init__.py
│   ├── models.py (FXTransact classes)
│   └── helpers.py
├── market/
│   ├── __init__.py
│   ├── timing.py
│   └── analysis.py
├── data/
│   ├── __init__.py
│   ├── processing.py
│   └── conversion.py
├── datetime/
│   ├── __init__.py
│   └── utils.py
└── constants/
    ├── __init__.py
    ├── trading.py
    └── general.py
```

### jgtutils (Utilities) 🔧
```
jgtutils/
├── __init__.py (utility API + jgtcore re-exports)
├── cli/
│   ├── __init__.py
│   ├── arguments.py
│   ├── helpers.py
│   └── constants.py
├── os/
│   ├── __init__.py
│   ├── paths.py
│   ├── fx_helpers.py
│   └── wsl_helpers.py
├── env/
│   ├── __init__.py
│   ├── loading.py
│   └── management.py
├── pov/
│   ├── __init__.py
│   └── calculations.py
└── scripts/
    └── (CLI entry points)
```

## Benefits

1. **🎯 Clear Separation**: Utilities vs Libraries properly separated
2. **🗑️ Reduced Duplication**: Remove duplicate configuration/settings code
3. **🔧 Better Maintainability**: Smaller, focused modules
4. **📦 Proper Dependencies**: Clean import structure
5. **♻️ Reusability**: Core libraries can be used independently
6. **🧪 Easier Testing**: Smaller modules are easier to test
7. **📚 Better Documentation**: Clear boundaries make documentation easier

## Risk Mitigation Strategy

### Backward Compatibility
- Maintain public API compatibility during transition
- Use deprecation warnings for old imports
- Provide migration guides for users

### Testing Strategy
- Comprehensive testing at each phase
- Automated tests for all moved functionality
- Integration tests for cross-module dependencies

### Rollout Strategy
- Gradual migration to avoid breaking changes
- Feature flags for new structure
- Parallel support during transition period

## Implementation Timeline

### Week 1-2: Phase 1 (Critical)
- Split jgtcommon.py
- Create new module structure
- Update immediate dependencies

### Week 3-4: Phase 2 (High Priority)
- Migrate trading libraries
- Update jgtcore structure
- Test trading functionality

### Week 5-6: Phase 3 (Medium Priority)
- Clean utilities structure
- Reorganize remaining modules
- Update CLI tools

### Week 7-8: Phase 4 (Finalization)
- Final import updates
- Documentation updates
- Comprehensive testing
- Release preparation

## Success Metrics

1. **Code Quality**: Reduction in file sizes, improved modularity
2. **Test Coverage**: Maintain or improve current test coverage
3. **Performance**: No performance regression
4. **Usability**: Simplified import structure
5. **Maintainability**: Easier to add new features and fix bugs

## Next Actions

1. **Immediate**: Begin Phase 1 - Split jgtcommon.py
2. **Priority**: Create jgtcore module structure  
3. **Critical**: Maintain backward compatibility throughout
4. **Essential**: Comprehensive testing at each step

---

*This refactoring plan represents a strategic approach to properly separate concerns and create a maintainable, scalable codebase architecture.*