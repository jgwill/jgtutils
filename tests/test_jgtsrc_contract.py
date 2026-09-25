"""What jgwill/jgtsrc imports from jgtutils. A change that fails here breaks jgtsrc.

Consumers, 2026-09-25:
- iprops.get_pips: jgt-data-server (signal_geometry), jgt-strategy-api (evaluator)
- iprops.get_iprop and iprops._key_for: jgt-transact (oanda_bridge, instrument_map)
- market_hours.is_instrument_market_open, filter_open_instruments,
  get_all_market_status: jgt-data-server (updater, routes), jgt-strategy-api

_key_for is private by name but consumed; rename it only with an alias.

Run against the installed package: pytest tests/test_jgtsrc_contract.py
"""
import inspect


def test_the_iprops_names_jgtsrc_imports_exist():
    from jgtutils.iprops import _key_for, get_iprop, get_pips
    for f in (get_pips, get_iprop, _key_for):
        assert callable(f)


def test_get_pips_answers_for_a_major():
    from jgtutils.iprops import get_pips
    assert abs(float(get_pips("EUR/USD")) - 0.0001) < 1e-12


def test_the_market_hours_names_jgtsrc_imports_exist():
    from jgtutils.market_hours import filter_open_instruments, get_all_market_status, is_instrument_market_open
    for f in (is_instrument_market_open, filter_open_instruments, get_all_market_status):
        assert callable(f)
    assert "instrument" in "".join(inspect.signature(is_instrument_market_open).parameters)
