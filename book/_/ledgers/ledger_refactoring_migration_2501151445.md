# Ledger: Refactoring and Migration Research
**Topic:** Full refactoring and separation of utilities and libraries for jgtutils → jgtcore migration
**Timestamp:** 2501151445
**Status:** COMPLETED - RESEARCH PHASE

## Intention
Research and produce a comprehensive refactoring plan to separate utilities and libraries, continuing the migration from jgtutils to jgtcore. This involves:
- Understanding current package structures
- Identifying what should be utilities vs libraries
- Creating a separation strategy
- Documenting the migration plan

## Current State Analysis
- **Migration Status**: Partially complete - jgtcore already exists and contains core library functions
- **Dependencies**: jgtutils → depends on jgtcore>=0.1.0
- **Import Pattern**: Core functions imported from jgtcore and re-exposed in jgtutils.__init__.py
- **Problem Areas**: Large monolithic files (jgtcommon.py = 2327 lines) with mixed responsibilities

## Tasks Status
- [x] Analyze jgtutils package structure and functionality
- [x] Analyze jgtcore package structure and current migration state
- [x] Review package configurations (pyproject.toml, setup.py)
- [x] Identify utilities vs libraries classification
- [x] Create comprehensive refactoring plan
- [x] Document migration strategy

## Key Findings

### Already Migrated to jgtcore
✅ **Core Library Functions** (imported from jgtcore):
- `get_config`, `get_setting`, `setup_environment`
- `get_config_value`, `is_demo_mode`
- `readconfig`, `load_settings`, `get_settings`
- `dt_from_last_week_as_string_fxformat`

### Current jgtutils Structure Analysis

#### 🔧 **UTILITIES** (Should stay in jgtutils)
1. **CLI Tools & Helpers**
   - `jgtclihelper.py` (44 lines) - JSON message formatting, signal handling
   - `jgtcliconstants.py` (195 lines) - CLI argument constants and groups
   - CLI test scripts: `cli_test_*.py` files

2. **OS & File System Utilities**
   - `jgtos.py` (325 lines) - File path utilities, data directory management
   - `jgtfxhelper.py` (137 lines) - FX-specific file helpers
   - `jgtwslhelper.py` (172 lines) - WSL-specific utilities

3. **Environment & Configuration Utilities**
   - `jgtenv.py` (105 lines) - Environment loading utilities
   - `jgtset.py` (404 lines) - Configuration management utilities

4. **POV (Point of View) Utilities**
   - `jgtpov.py` (304 lines) - Timeframe calculations and date handling

#### 📚 **LIBRARIES** (Should migrate to jgtcore)
1. **Trading Domain Logic**
   - `FXTransact.py` (1019 lines) - Core trading data structures and business logic
   - Trading-specific constants from `jgtconstants.py` (trading indicators, signals)

2. **Data Processing Libraries**
   - Column manipulation utilities from various helper files
   - Type conversion helpers (`coltypehelper.py`, `colconverthelper.py`)

#### ⚠️ **MIXED RESPONSIBILITY** (Needs refactoring)
1. **jgtcommon.py** (2327 lines) - **CRITICAL REFACTOR NEEDED**
   - CLI argument parsing (→ utilities)
   - Settings management (→ already in jgtcore, remove duplicates)
   - Configuration loading (→ already in jgtcore, remove duplicates)
   - Market timing functions (→ libraries)
   - Date/time utilities (→ libraries)

## COMPREHENSIVE REFACTORING PLAN

### Phase 1: Split jgtcommon.py (HIGH PRIORITY)
```
jgtcommon.py (2327 lines) →
├── jgtcliarguments.py (CLI parsing utilities - stay in jgtutils)
├── jgtmarket.py (Market timing - move to jgtcore)
├── jgtdatetime.py (Date/time utilities - move to jgtcore)
└── Remove duplicates (already in jgtcore)
```

### Phase 2: Migrate Trading Libraries to jgtcore
```
jgtutils/ → jgtcore/
├── FXTransact.py → jgtcore/trading/
├── Trading constants → jgtcore/constants/
├── Market utilities → jgtcore/market/
└── Data processing → jgtcore/data/
```

### Phase 3: Clean Utilities Structure
```
jgtutils/ (utilities only)
├── cli/ (CLI tools and helpers)
├── os/ (OS and file system utilities)
├── env/ (Environment utilities)
└── pov/ (POV utilities)
```

### Phase 4: Update Dependencies and Imports
1. Update jgtcore with new library modules
2. Update jgtutils imports to use jgtcore for library functions
3. Remove duplicate code
4. Update CLI scripts to use proper separation

### Benefits
1. **Clear Separation**: Utilities vs Libraries properly separated
2. **Reduced Duplication**: Remove duplicate configuration/settings code
3. **Better Maintainability**: Smaller, focused modules
4. **Proper Dependencies**: Clean import structure
5. **Reusability**: Core libraries can be used independently

### Recommended Module Structure

#### jgtcore (Libraries)
```
jgtcore/
├── __init__.py (core API)
├── config/ (configuration management)
├── trading/ (FXTransact and trading logic)
├── market/ (market timing and analysis)
├── data/ (data processing utilities)
├── datetime/ (date/time utilities)
└── constants/ (trading constants)
```

#### jgtutils (Utilities)
```
jgtutils/
├── __init__.py (utility API + jgtcore re-exports)
├── cli/ (CLI tools and argument parsing)
├── os/ (file system and OS utilities)
├── env/ (environment management)
├── pov/ (POV calculations)
└── scripts/ (CLI entry points)
```

## Evolution
**RESEARCH COMPLETED** - Comprehensive refactoring plan created

### Next Steps
1. Begin Phase 1: Split jgtcommon.py
2. Create jgtcore module structure
3. Migrate trading libraries
4. Update imports and dependencies
5. Test migration thoroughly

### Risk Mitigation
- Maintain backward compatibility during transition
- Comprehensive testing at each phase
- Gradual migration to avoid breaking changes
- Clear documentation of new structure