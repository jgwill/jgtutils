"""
Market Hours — Per-instrument trading schedule awareness for FXCM.

Classifies instruments into categories (FOREX, INDEX, COMMODITY, METAL, BOND)
and provides per-category market open/close/daily-break schedules so that
schedulers can skip refreshes when instruments are not tradable.

FXCM Trading Hours (all times UTC):
  Forex:       Sunday 22:00 → Friday 21:55  (no daily break)
  Indices:     Sunday 23:00 → Friday 21:45  (daily break 22:00-23:00)
  Commodities: Sunday 23:00 → Friday 21:45  (daily break 22:00-23:00)
  Metals:      Sunday 23:00 → Friday 21:45  (daily break 22:00-23:00)
  Bonds:       Sunday 23:00 → Friday 21:45  (daily break 22:00-23:00)

Usage:
    from jgtutils.market_hours import is_instrument_market_open, get_instrument_category
    
    if is_instrument_market_open("EUR/USD"):
        # safe to refresh
    
    status = get_all_market_status(["EUR/USD", "SPX500", "XAU/USD"])
"""

from datetime import datetime, time, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple


class InstrumentCategory(str, Enum):
    FOREX = "forex"
    INDEX = "index"
    COMMODITY = "commodity"
    METAL = "metal"
    BOND = "bond"


# ── Instrument → Category mapping ───────────────────────────────────
# Based on FXCM offer IDs: 1-105=forex, 1000+=index, 2000+=commodity,
# 3000+=bond, 4000+=metal.  Explicit mapping for safety.

_INSTRUMENT_CATEGORIES: Dict[str, InstrumentCategory] = {
    # Forex (major + cross + exotic)
    "EUR/USD": InstrumentCategory.FOREX,
    "USD/JPY": InstrumentCategory.FOREX,
    "GBP/USD": InstrumentCategory.FOREX,
    "USD/CHF": InstrumentCategory.FOREX,
    "EUR/CHF": InstrumentCategory.FOREX,
    "AUD/USD": InstrumentCategory.FOREX,
    "USD/CAD": InstrumentCategory.FOREX,
    "NZD/USD": InstrumentCategory.FOREX,
    "EUR/GBP": InstrumentCategory.FOREX,
    "EUR/JPY": InstrumentCategory.FOREX,
    "GBP/JPY": InstrumentCategory.FOREX,
    "CHF/JPY": InstrumentCategory.FOREX,
    "GBP/CHF": InstrumentCategory.FOREX,
    "EUR/AUD": InstrumentCategory.FOREX,
    "EUR/CAD": InstrumentCategory.FOREX,
    "AUD/CAD": InstrumentCategory.FOREX,
    "AUD/JPY": InstrumentCategory.FOREX,
    "CAD/JPY": InstrumentCategory.FOREX,
    "NZD/JPY": InstrumentCategory.FOREX,
    "GBP/CAD": InstrumentCategory.FOREX,
    "GBP/NZD": InstrumentCategory.FOREX,
    "GBP/AUD": InstrumentCategory.FOREX,
    "AUD/NZD": InstrumentCategory.FOREX,
    "USD/SEK": InstrumentCategory.FOREX,
    "EUR/SEK": InstrumentCategory.FOREX,
    "EUR/NOK": InstrumentCategory.FOREX,
    "USD/NOK": InstrumentCategory.FOREX,
    "USD/MXN": InstrumentCategory.FOREX,
    "AUD/CHF": InstrumentCategory.FOREX,
    "EUR/NZD": InstrumentCategory.FOREX,
    "USD/ZAR": InstrumentCategory.FOREX,
    "USD/HKD": InstrumentCategory.FOREX,
    "ZAR/JPY": InstrumentCategory.FOREX,
    "USD/TRY": InstrumentCategory.FOREX,
    "EUR/TRY": InstrumentCategory.FOREX,
    "NZD/CHF": InstrumentCategory.FOREX,
    "CAD/CHF": InstrumentCategory.FOREX,
    "NZD/CAD": InstrumentCategory.FOREX,
    "TRY/JPY": InstrumentCategory.FOREX,
    "USD/CNH": InstrumentCategory.FOREX,
    "EUR/HUF": InstrumentCategory.FOREX,
    "USD/HUF": InstrumentCategory.FOREX,
    # Indices
    "SPX500": InstrumentCategory.INDEX,
    "US30": InstrumentCategory.INDEX,
    "NAS100": InstrumentCategory.INDEX,
    "US2000": InstrumentCategory.INDEX,
    "USDOLLAR": InstrumentCategory.INDEX,
    "AUS200": InstrumentCategory.INDEX,
    "GER30": InstrumentCategory.INDEX,
    "FRA40": InstrumentCategory.INDEX,
    "UK100": InstrumentCategory.INDEX,
    "ESP35": InstrumentCategory.INDEX,
    "HKG33": InstrumentCategory.INDEX,
    "JPN225": InstrumentCategory.INDEX,
    "EUSTX50": InstrumentCategory.INDEX,
    # Commodities
    "USOil": InstrumentCategory.COMMODITY,
    "UKOil": InstrumentCategory.COMMODITY,
    "NGAS": InstrumentCategory.COMMODITY,
    "SOYF": InstrumentCategory.COMMODITY,
    "WHEATF": InstrumentCategory.COMMODITY,
    "CORNF": InstrumentCategory.COMMODITY,
    "Copper": InstrumentCategory.COMMODITY,
    # Metals
    "XAU/USD": InstrumentCategory.METAL,
    "XAG/USD": InstrumentCategory.METAL,
    # Bonds
    "Bund": InstrumentCategory.BOND,
    "Bobl": InstrumentCategory.BOND,
    "Schatz": InstrumentCategory.BOND,
    "2USNote": InstrumentCategory.BOND,
    "5USNote": InstrumentCategory.BOND,
    "10USNote": InstrumentCategory.BOND,
    "FED30D": InstrumentCategory.BOND,
    "EURIBOR3M": InstrumentCategory.BOND,
    "SONIA3M": InstrumentCategory.BOND,
}


# ── Per-category trading schedules (UTC) ─────────────────────────────
# Each schedule: (week_open_day, week_open_time, week_close_day, week_close_time,
#                 daily_break_start, daily_break_end)
# Days: 0=Monday ... 6=Sunday

class MarketSchedule:
    """Trading schedule for an instrument category."""

    def __init__(
        self,
        week_open_day: int,   # weekday when market opens (6=Sunday)
        week_open_time: time,  # UTC time of weekly open
        week_close_day: int,  # weekday when market closes (4=Friday)
        week_close_time: time,  # UTC time of weekly close
        daily_break_start: Optional[time] = None,  # daily break start (UTC)
        daily_break_end: Optional[time] = None,     # daily break end (UTC)
    ):
        self.week_open_day = week_open_day
        self.week_open_time = week_open_time
        self.week_close_day = week_close_day
        self.week_close_time = week_close_time
        self.daily_break_start = daily_break_start
        self.daily_break_end = daily_break_end

    def is_open(self, dt: Optional[datetime] = None) -> bool:
        """Check if market is open at the given UTC datetime."""
        if dt is None:
            dt = datetime.utcnow()

        day = dt.weekday()  # 0=Mon ... 6=Sun
        t = dt.time()

        # Saturday: always closed for all FXCM instruments
        if day == 5:
            return False

        # Sunday: only open after weekly open time
        if day == 6:
            return t >= self.week_open_time

        # Friday: only open before weekly close time
        if day == self.week_close_day:
            if t >= self.week_close_time:
                return False

        # Monday-Thursday (and Friday before close): check daily break
        if self.daily_break_start and self.daily_break_end:
            if self.daily_break_start <= t < self.daily_break_end:
                return False

        return True

    def next_open(self, dt: Optional[datetime] = None) -> datetime:
        """Calculate next market open time from given UTC datetime."""
        if dt is None:
            dt = datetime.utcnow()

        # If already open, return current time
        if self.is_open(dt):
            return dt

        day = dt.weekday()
        t = dt.time()

        # If in daily break, next open is break end today
        if self.daily_break_start and self.daily_break_end:
            if self.daily_break_start <= t < self.daily_break_end:
                return dt.replace(
                    hour=self.daily_break_end.hour,
                    minute=self.daily_break_end.minute,
                    second=0, microsecond=0
                )

        # Otherwise, next open is the weekly open
        days_until_open = (self.week_open_day - day) % 7
        if days_until_open == 0 and t >= self.week_open_time:
            days_until_open = 7
        from datetime import timedelta
        next_day = dt + timedelta(days=days_until_open)
        return next_day.replace(
            hour=self.week_open_time.hour,
            minute=self.week_open_time.minute,
            second=0, microsecond=0
        )


# ── Schedule definitions ─────────────────────────────────────────────

FOREX_SCHEDULE = MarketSchedule(
    week_open_day=6,        # Sunday
    week_open_time=time(22, 0),   # 22:00 UTC (5:00 PM ET)
    week_close_day=4,       # Friday
    week_close_time=time(21, 55),  # 21:55 UTC (4:55 PM ET)
    daily_break_start=None,
    daily_break_end=None,
)

# Indices, Commodities, Metals, Bonds all share the same FXCM schedule
CFD_SCHEDULE = MarketSchedule(
    week_open_day=6,        # Sunday
    week_open_time=time(23, 0),   # 23:00 UTC
    week_close_day=4,       # Friday
    week_close_time=time(21, 45),  # 21:45 UTC
    daily_break_start=time(22, 0),  # 22:00 UTC
    daily_break_end=time(23, 0),    # 23:00 UTC
)

_CATEGORY_SCHEDULES: Dict[InstrumentCategory, MarketSchedule] = {
    InstrumentCategory.FOREX: FOREX_SCHEDULE,
    InstrumentCategory.INDEX: CFD_SCHEDULE,
    InstrumentCategory.COMMODITY: CFD_SCHEDULE,
    InstrumentCategory.METAL: CFD_SCHEDULE,
    InstrumentCategory.BOND: CFD_SCHEDULE,
}


# ── Public API ───────────────────────────────────────────────────────

def get_instrument_category(instrument: str) -> InstrumentCategory:
    """Get category for an instrument. Defaults to FOREX for unknown instruments."""
    return _INSTRUMENT_CATEGORIES.get(instrument, InstrumentCategory.FOREX)


def get_schedule(instrument: str) -> MarketSchedule:
    """Get trading schedule for an instrument."""
    cat = get_instrument_category(instrument)
    return _CATEGORY_SCHEDULES[cat]


def is_instrument_market_open(instrument: str, current_time: Optional[datetime] = None) -> bool:
    """Check if a specific instrument's market is currently open.
    
    Args:
        instrument: Instrument symbol (e.g. "EUR/USD", "SPX500")
        current_time: UTC datetime to check. Uses utcnow() if None.
    
    Returns:
        True if the instrument is tradable at the given time.
    """
    schedule = get_schedule(instrument)
    return schedule.is_open(current_time)


def filter_open_instruments(instruments: List[str], current_time: Optional[datetime] = None) -> List[str]:
    """Filter a list of instruments to only those with open markets.
    
    Args:
        instruments: List of instrument symbols
        current_time: UTC datetime. Uses utcnow() if None.
    
    Returns:
        List of instruments whose markets are currently open.
    """
    if current_time is None:
        current_time = datetime.utcnow()
    return [i for i in instruments if is_instrument_market_open(i, current_time)]


def get_all_market_status(instruments: List[str], current_time: Optional[datetime] = None) -> Dict:
    """Get market open/closed status for all instruments.
    
    Returns dict with per-instrument and per-category status.
    """
    if current_time is None:
        current_time = datetime.utcnow()

    statuses = {}
    for instrument in instruments:
        cat = get_instrument_category(instrument)
        schedule = get_schedule(instrument)
        is_open = schedule.is_open(current_time)
        statuses[instrument] = {
            "category": cat.value,
            "is_open": is_open,
            "next_open": schedule.next_open(current_time).isoformat() if not is_open else None,
        }

    # Summary by category
    categories = {}
    for cat in InstrumentCategory:
        sched = _CATEGORY_SCHEDULES[cat]
        categories[cat.value] = {
            "is_open": sched.is_open(current_time),
        }

    return {
        "timestamp_utc": current_time.isoformat(),
        "day": current_time.strftime("%A"),
        "instruments": statuses,
        "categories": categories,
    }
