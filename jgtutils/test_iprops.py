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
        assert iprops.get_pips("XAG-USD", "fxcm") == 0.01
        assert iprops.get_pips("XAG-USD", "oanda") == 0.0001

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
        assert iprops.get_pips(fxcm, "fxcm") != iprops.get_pips(oanda, "oanda")

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
        assert iprops.get_pips(instrument, "oanda") == pips

    def test_the_fxcm_half_kept_its_values(self):
        # Adding a broker must not have moved anything that was already right.
        assert iprops.get_pips("XAU/USD") == 0.01
        assert iprops.get_pips("EUR/USD") == 0.0001
        assert iprops.get_iprop("EUR-USD")["bu"] == 1000


class TestPunctuationIsNotABroker:
    """EUR/USD, EUR-USD and EUR_USD are one instrument.

    Which of them a caller types says nothing about which broker they trade on.
    1.0.28 let the underscore select OANDA and the dash select FXCM, so silver
    resolved to two different pip sizes depending on how it was spelled. The
    contract is now named, not spelled.
    """

    FORMS = ["XAG/USD", "XAG-USD", "XAG_USD"]

    @pytest.mark.parametrize("broker,pips", [("fxcm", 0.01), ("oanda", 0.0001)])
    def test_every_spelling_gives_one_answer_per_broker(self, broker, pips):
        for form in self.FORMS:
            assert iprops.get_pips(form, broker) == pips, form

    @pytest.mark.parametrize("name,identity", [
        ("EUR/USD", "EUR-USD"), ("EUR_USD", "EUR-USD"), ("EUR-USD", "EUR-USD"),
        ("XCU_USD", "Copper"), ("Copper", "Copper"),
        ("SPX500_USD", "SPX500"), ("SPX500", "SPX500"),
        ("WTICO_USD", "USOil"), ("NATGAS_USD", "NGAS"),
    ])
    def test_one_identity_under_every_name(self, name, identity):
        assert iprops.canonical(name) == identity

    def test_the_broker_can_come_from_the_environment(self, monkeypatch):
        monkeypatch.setenv("BROKER_PROVIDER", "oanda")
        assert iprops.get_pips("XAG-USD") == 0.0001
        monkeypatch.setenv("JGT_BROKER", "fxcm")   # more specific wins
        assert iprops.get_pips("XAG-USD") == 0.01

    def test_an_unqualified_lookup_still_means_what_it_always_meant(self, monkeypatch):
        monkeypatch.delenv("JGT_BROKER", raising=False)
        monkeypatch.delenv("BROKER_PROVIDER", raising=False)
        assert iprops.get_pips("XAG-USD") == 0.01

    def test_which_brokers_carry_an_instrument(self):
        assert iprops.get_brokers_for("EUR/USD") == ("fxcm", "oanda")
        assert iprops.get_brokers_for("XPT-USD") == ("oanda",)   # platinum, OANDA only
        assert iprops.get_brokers_for("NOT-REAL") == ()

    def test_every_fxcm_instrument_is_also_on_oanda(self):
        # Measured 2026-09-09: all 48 have an OANDA counterpart, so a stack
        # switching brokers loses no instrument — only, for eight of them, the
        # pip size changes.
        fxcm = [k for k, v in iprops.data.items() if v["broker"] == "fxcm"]
        assert [k for k in fxcm if "oanda" not in iprops.get_brokers_for(k)] == []

    def test_an_instrument_a_broker_lacks_says_so(self):
        with pytest.raises(KeyError, match="fxcm does not carry"):
            iprops.get_pips("XPT_USD", "fxcm")

    def test_an_unknown_broker_is_refused(self):
        with pytest.raises(ValueError, match="unknown broker"):
            iprops.get_pips("EUR-USD", "ig")


class TestOrderSizing:
    """A size has to land on the instrument's own step, not a shared one.

    `1` meaning "one minimum position" only works if both the minimum and the
    step it moves in come from the broker. Gold trades from 0.1 of a unit in
    tenths, an index from 0.01 in hundredths, a currency pair from 1 in whole
    units — one shared lot size cannot express any two of those.
    """

    @pytest.mark.parametrize("instrument,minimum,precision", [
        ("EUR_USD", 1.0, 0),
        ("XAU_USD", 0.1, 1),
        ("XAG_USD", 1.0, 0),
        ("SPX500_USD", 0.01, 2),
        ("DE30_EUR", 0.01, 2),
    ])
    def test_the_minimum_and_its_step(self, instrument, minimum, precision):
        prop = iprops.get_iprop(instrument, "oanda")
        assert prop["qtmi"] == pytest.approx(minimum)
        assert prop["qtpre"] == precision

    def test_every_oanda_entry_carries_both(self):
        for name, prop in iprops.data.items():
            if prop["broker"] == "oanda":
                assert "qtmi" in prop and "qtpre" in prop, name

    def test_the_minimum_is_expressible_at_its_own_precision(self):
        for name, prop in iprops.data.items():
            if prop["broker"] != "oanda" or not prop["qtmi"]:
                continue
            assert round(prop["qtmi"], prop["qtpre"]) == pytest.approx(prop["qtmi"]), name
