"""Tests for market_hours module — FXCM per-instrument trading schedule."""

import unittest
from datetime import datetime, time

from jgtutils.market_hours import (
    InstrumentCategory,
    get_instrument_category,
    is_instrument_market_open,
    filter_open_instruments,
    get_all_market_status,
    FOREX_SCHEDULE,
    CFD_SCHEDULE,
)


class TestInstrumentCategories(unittest.TestCase):
    def test_forex_pairs(self):
        self.assertEqual(get_instrument_category("EUR/USD"), InstrumentCategory.FOREX)
        self.assertEqual(get_instrument_category("GBP/USD"), InstrumentCategory.FOREX)
        self.assertEqual(get_instrument_category("USD/JPY"), InstrumentCategory.FOREX)

    def test_indices(self):
        self.assertEqual(get_instrument_category("SPX500"), InstrumentCategory.INDEX)
        self.assertEqual(get_instrument_category("US30"), InstrumentCategory.INDEX)
        self.assertEqual(get_instrument_category("NAS100"), InstrumentCategory.INDEX)
        self.assertEqual(get_instrument_category("AUS200"), InstrumentCategory.INDEX)

    def test_commodities(self):
        self.assertEqual(get_instrument_category("USOil"), InstrumentCategory.COMMODITY)
        self.assertEqual(get_instrument_category("NGAS"), InstrumentCategory.COMMODITY)

    def test_metals(self):
        self.assertEqual(get_instrument_category("XAU/USD"), InstrumentCategory.METAL)
        self.assertEqual(get_instrument_category("XAG/USD"), InstrumentCategory.METAL)

    def test_bonds(self):
        self.assertEqual(get_instrument_category("Bund"), InstrumentCategory.BOND)
        self.assertEqual(get_instrument_category("10USNote"), InstrumentCategory.BOND)

    def test_unknown_defaults_forex(self):
        self.assertEqual(get_instrument_category("UNKNOWN/XYZ"), InstrumentCategory.FOREX)


class TestForexSchedule(unittest.TestCase):
    """Forex: Sunday 22:00 UTC → Friday 21:55 UTC, no daily break."""

    def test_monday_midday_open(self):
        dt = datetime(2026, 3, 2, 12, 0)  # Monday
        self.assertTrue(is_instrument_market_open("EUR/USD", dt))

    def test_wednesday_night_open(self):
        dt = datetime(2026, 3, 4, 23, 30)  # Wednesday 23:30
        self.assertTrue(is_instrument_market_open("EUR/USD", dt))

    def test_friday_before_close_open(self):
        dt = datetime(2026, 3, 6, 21, 0)  # Friday 21:00 (before 21:55)
        self.assertTrue(is_instrument_market_open("EUR/USD", dt))

    def test_friday_after_close_closed(self):
        dt = datetime(2026, 3, 6, 21, 55)  # Friday 21:55 (at close)
        self.assertFalse(is_instrument_market_open("EUR/USD", dt))

    def test_friday_late_closed(self):
        dt = datetime(2026, 3, 6, 23, 0)  # Friday 23:00
        self.assertFalse(is_instrument_market_open("EUR/USD", dt))

    def test_saturday_closed(self):
        dt = datetime(2026, 3, 7, 12, 0)  # Saturday
        self.assertFalse(is_instrument_market_open("EUR/USD", dt))

    def test_sunday_before_open_closed(self):
        dt = datetime(2026, 3, 8, 10, 0)  # Sunday 10:00
        self.assertFalse(is_instrument_market_open("EUR/USD", dt))

    def test_sunday_at_open(self):
        dt = datetime(2026, 3, 8, 22, 0)  # Sunday 22:00 (open time)
        self.assertTrue(is_instrument_market_open("EUR/USD", dt))

    def test_sunday_after_open(self):
        dt = datetime(2026, 3, 8, 22, 30)  # Sunday 22:30
        self.assertTrue(is_instrument_market_open("EUR/USD", dt))

    def test_no_daily_break(self):
        # Forex has no daily break — 22:30 on a Tuesday is open
        dt = datetime(2026, 3, 3, 22, 30)  # Tuesday 22:30
        self.assertTrue(is_instrument_market_open("EUR/USD", dt))


class TestCFDSchedule(unittest.TestCase):
    """Indices/Commodities/Metals: Sunday 23:00 → Friday 21:45, daily break 22:00-23:00."""

    def test_monday_midday_open(self):
        dt = datetime(2026, 3, 2, 12, 0)  # Monday noon
        self.assertTrue(is_instrument_market_open("SPX500", dt))

    def test_daily_break_closed(self):
        dt = datetime(2026, 3, 3, 22, 30)  # Tuesday 22:30 (in daily break)
        self.assertFalse(is_instrument_market_open("SPX500", dt))

    def test_daily_break_start_closed(self):
        dt = datetime(2026, 3, 3, 22, 0)  # Tuesday 22:00 (break start)
        self.assertFalse(is_instrument_market_open("SPX500", dt))

    def test_daily_break_end_open(self):
        dt = datetime(2026, 3, 3, 23, 0)  # Tuesday 23:00 (break end — open)
        self.assertTrue(is_instrument_market_open("SPX500", dt))

    def test_before_daily_break_open(self):
        dt = datetime(2026, 3, 3, 21, 59)  # Tuesday 21:59 (before break)
        self.assertTrue(is_instrument_market_open("SPX500", dt))

    def test_friday_close(self):
        dt = datetime(2026, 3, 6, 21, 45)  # Friday 21:45
        self.assertFalse(is_instrument_market_open("SPX500", dt))

    def test_friday_before_close_open(self):
        dt = datetime(2026, 3, 6, 21, 44)  # Friday 21:44
        self.assertTrue(is_instrument_market_open("SPX500", dt))

    def test_saturday_closed(self):
        dt = datetime(2026, 3, 7, 12, 0)
        self.assertFalse(is_instrument_market_open("SPX500", dt))

    def test_sunday_before_open_closed(self):
        dt = datetime(2026, 3, 8, 22, 0)  # Sunday 22:00
        self.assertFalse(is_instrument_market_open("SPX500", dt))

    def test_sunday_at_open(self):
        dt = datetime(2026, 3, 8, 23, 0)  # Sunday 23:00
        self.assertTrue(is_instrument_market_open("SPX500", dt))

    def test_xauusd_daily_break(self):
        dt = datetime(2026, 3, 4, 22, 15)  # Wednesday 22:15 (in break)
        self.assertFalse(is_instrument_market_open("XAU/USD", dt))

    def test_xauusd_after_break(self):
        dt = datetime(2026, 3, 4, 23, 1)  # Wednesday 23:01
        self.assertTrue(is_instrument_market_open("XAU/USD", dt))

    def test_usoil_daily_break(self):
        dt = datetime(2026, 3, 4, 22, 30)
        self.assertFalse(is_instrument_market_open("USOil", dt))


class TestFilterOpenInstruments(unittest.TestCase):
    def test_weekend_filters_all(self):
        instruments = ["EUR/USD", "SPX500", "XAU/USD"]
        dt = datetime(2026, 3, 7, 12, 0)  # Saturday
        result = filter_open_instruments(instruments, dt)
        self.assertEqual(result, [])

    def test_weekday_all_open(self):
        instruments = ["EUR/USD", "SPX500", "XAU/USD"]
        dt = datetime(2026, 3, 3, 15, 0)  # Tuesday 15:00
        result = filter_open_instruments(instruments, dt)
        self.assertEqual(result, instruments)

    def test_daily_break_filters_cfds_only(self):
        instruments = ["EUR/USD", "SPX500", "XAU/USD"]
        dt = datetime(2026, 3, 3, 22, 30)  # Tuesday 22:30 (CFD daily break)
        result = filter_open_instruments(instruments, dt)
        # Only forex should remain — indices and metals in daily break
        self.assertEqual(result, ["EUR/USD"])

    def test_sunday_evening_forex_only(self):
        instruments = ["EUR/USD", "SPX500", "XAU/USD"]
        dt = datetime(2026, 3, 8, 22, 30)  # Sunday 22:30
        # Forex opens 22:00, CFDs open 23:00
        result = filter_open_instruments(instruments, dt)
        self.assertEqual(result, ["EUR/USD"])


class TestMarketStatus(unittest.TestCase):
    def test_status_structure(self):
        instruments = ["EUR/USD", "SPX500"]
        dt = datetime(2026, 3, 3, 15, 0)
        status = get_all_market_status(instruments, dt)
        self.assertIn("instruments", status)
        self.assertIn("categories", status)
        self.assertIn("EUR/USD", status["instruments"])
        self.assertEqual(status["instruments"]["EUR/USD"]["category"], "forex")
        self.assertTrue(status["instruments"]["EUR/USD"]["is_open"])

    def test_status_weekend(self):
        instruments = ["EUR/USD", "SPX500"]
        dt = datetime(2026, 3, 7, 12, 0)  # Saturday
        status = get_all_market_status(instruments, dt)
        self.assertFalse(status["instruments"]["EUR/USD"]["is_open"])
        self.assertIsNotNone(status["instruments"]["EUR/USD"]["next_open"])


if __name__ == "__main__":
    unittest.main()
