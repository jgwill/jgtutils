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


class TestTwoBrokers:
    """A pip size means nothing without the contract it is quoted on.

    The table describes FXCM under dash and single-token names, and OANDA under
    its own underscore names. Seven instruments are genuinely quoted differently
    by the two brokers, so neither value is wrong and neither may overwrite the
    other. See jgwill/jgtutils#26.
    """

    def test_every_entry_names_its_broker(self):
        for name, prop in iprops.data.items():
            assert prop["broker"] in ("fxcm", "oanda"), name

    def test_both_brokers_are_present(self):
        brokers = {p["broker"] for p in iprops.data.values()}
        assert brokers == {"fxcm", "oanda"}

    def test_silver_differs_by_broker_and_both_survive(self):
        # FXCM quotes silver to 2 decimals, OANDA to 5. Collapsing these into
        # one entry misprices a silver stop by 100x on whichever broker loses.
        assert iprops.get_pips("XAG-USD") == 0.01
        assert iprops.get_pips("XAG_USD") == 0.0001

    @pytest.mark.parametrize("fxcm,oanda", [
        ("SPX500", "SPX500_USD"),
        ("US2000", "US2000_USD"),
        ("NGAS", "NATGAS_USD"),
        ("Copper", "XCU_USD"),
        ("CORNF", "CORN_USD"),
        ("SOYF", "SOYBN_USD"),
        ("WHEATF", "WHEAT_USD"),
    ])
    def test_the_instruments_the_brokers_quote_differently(self, fxcm, oanda):
        assert iprops.get_pips(fxcm) != iprops.get_pips(oanda)

    @pytest.mark.parametrize("instrument,pips", [
        ("XAU_USD", 0.01),
        ("EUR_USD", 0.0001),
        ("USD_JPY", 0.01),
        ("SPX500_USD", 1.0),
        ("NAS100_USD", 1.0),
        ("WTICO_USD", 0.01),
        ("XPT_USD", 0.01),      # platinum — no FXCM entry has ever existed
        ("USB10Y_USD", 0.01),   # treasury
        ("USD_MXN", 0.0001),
    ])
    def test_oanda_instruments_resolve(self, instrument, pips):
        assert iprops.get_pips(instrument) == pips

    def test_the_fxcm_half_kept_its_values(self):
        # Adding a broker must not have moved anything that was already right.
        assert iprops.get_pips("XAU/USD") == 0.01
        assert iprops.get_pips("EUR/USD") == 0.0001
        assert iprops.get_iprop("EUR-USD")["bu"] == 1000
