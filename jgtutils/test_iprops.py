"""The instrument table holds instruments, and each one only once.

Until 1.0.27 the embedded JSON carried the whole 48-instrument map twice: once
at the top level, and again nested under a key literally named "all". That key
parsed as a 49th instrument with no `pips` field, so `get_pips("all")` raised
KeyError from inside the property lookup rather than saying the instrument was
unknown, and any caller enumerating the table saw a phantom entry.

The duplicate also made the file its own second source of truth — editing one
copy and not the other would have gone unnoticed, because `json.loads` keeps
the last of two identical keys and nothing compared them.
"""
import pytest

from jgtutils import iprops


def test_no_phantom_instrument():
    assert "all" not in iprops.data


def test_every_entry_is_an_instrument():
    for name, prop in iprops.data.items():
        assert "pips" in prop, f"{name} carries no pip size"
        assert "i" in prop, f"{name} carries no display name"


@pytest.mark.parametrize("instrument,pips", [
    ("XAU/USD", 0.01),     # metal
    ("XAG/USD", 0.01),
    ("EUR/USD", 0.0001),   # pair
    ("USD/JPY", 0.01),     # JPY cross
    ("SPX500", 0.1),       # index — quoted finer than a whole point
    ("NAS100", 1.0),
    ("USOil", 0.01),       # energy
    ("Copper", 0.001),
])
def test_pip_sizes_that_callers_depend_on(instrument, pips):
    assert iprops.get_pips(instrument) == pips


def test_slash_and_dash_name_the_same_instrument():
    assert iprops.get_iprop("XAU/USD") == iprops.get_iprop("XAU-USD")
