#!/usr/bin/env python3
"""Regenerate the OANDA half of `jgtutils/iprops.py` from the live broker.

The FXCM entries in that table were transcribed once and have been maintained
by hand ever since. The OANDA entries are not: they are read from
`GET /v3/accounts/{id}/instruments`, which reports `pipLocation`,
`displayPrecision`, `marginRate` and the order-size bounds for every instrument
the account can trade. Rerunning this script after a contract change produces a
diff rather than a discrepancy nobody notices.

Pip size is `10 ** pipLocation`. OANDA states it as an exponent precisely
because it is the decimal place a pip occupies, so the exponent is the fact and
the decimal is the rendering.

Usage
-----
    OANDA_TOKEN=... OANDA_ACCOUNT_ID=... python scripts/gen_oanda_iprops.py
    python scripts/gen_oanda_iprops.py --payload instruments.json

`--payload` takes a previously saved API response, so the table can be rebuilt
without credentials or a network round trip.

The FXCM entries are never touched: they keep their dash and single-token names
and their own pip sizes, which genuinely differ from OANDA's for seven
instruments (SPX500, US2000, NGAS, Copper, and the three grains). See
jgwill/jgtutils#26.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
IPROPS = REPO / "jgtutils" / "iprops.py"

PRACTICE = "https://api-fxpractice.oanda.com"
LIVE = "https://api-fxtrade.oanda.com"


def fetch_instruments(token: str, account_id: str, host: str) -> list[dict]:
    url = f"{host}/v3/accounts/{account_id}/instruments"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["instruments"]


def pip_size(instrument: dict) -> float:
    """`pipLocation` is the decimal place a pip occupies, as an exponent."""
    return round(10.0 ** instrument["pipLocation"], 10)


def as_iprop(instrument: dict) -> dict:
    """One OANDA instrument in the shape iprops has always used."""
    name = instrument["name"]
    margin = float(instrument.get("marginRate") or 0.0)
    return {
        "mar": {
            # OANDA states a margin *rate*; FXCM stated per-lot amounts. A rate
            # is not those numbers, so it is carried under its own key and the
            # FXCM-shaped fields stay honestly empty.
            "MMR": -1.0,
            "LMR": -1.0,
            "rate": margin,
        },
        "pre": instrument["displayPrecision"],
        "pips": pip_size(instrument),
        "cm": 1.0,
        "tsmi": 10,
        "tsmx": 300,
        "subs": True,
        # No "bu": FXCM quoted a base-unit size (1000 for a pair); OANDA trades
        # in units directly and reports no equivalent. A fabricated 1 would read
        # like a measurement, so the key is absent instead.
        "qtmi": float(instrument.get("minimumTradeSize") or 0),
        "qtmx": int(float(instrument.get("maximumOrderUnits") or 0)),
        # Decimals allowed in an order's unit count. Gold trades to 0.1 of a
        # unit, an index to 0.01, a currency pair only in whole units — so a
        # size has to be rounded to the instrument's own step, not a shared one.
        "qtpre": int(instrument.get("tradeUnitsPrecision") or 0),
        "cc": name.split("_")[-1],
        "i": instrument.get("displayName", name.replace("_", "/")),
        "broker": "oanda",
        "type": instrument["type"],
    }


def load_existing() -> dict:
    source = IPROPS.read_text()
    start = source.index('_json_iprops="""') + len('_json_iprops="""')
    end = source.index('"""', start)
    return json.loads(source[start:end]), source, start, end


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", type=Path, help="saved API response")
    parser.add_argument("--live", action="store_true", help="use the live host")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.payload:
        instruments = json.loads(args.payload.read_text())["instruments"]
    else:
        token = os.environ.get("OANDA_TOKEN")
        account = os.environ.get("OANDA_ACCOUNT_ID")
        if not token or not account:
            print("OANDA_TOKEN and OANDA_ACCOUNT_ID must be set", file=sys.stderr)
            return 2
        instruments = fetch_instruments(token, account, LIVE if args.live else PRACTICE)

    table, source, start, end = load_existing()

    # The FXCM entries predate any broker field; say so rather than leave it
    # ambiguous, because a pip size means nothing without the contract it is on.
    for name, prop in table.items():
        if prop.get("broker") is None:
            prop["broker"] = "fxcm"

    added = updated = 0
    for instrument in instruments:
        entry = as_iprop(instrument)
        name = instrument["name"]
        if name in table:
            updated += table[name] != entry
        else:
            added += 1
        table[name] = entry

    rendered = json.dumps(dict(sorted(table.items())), indent=2)
    print(f"{len(table)} entries — {added} added, {updated} updated")

    if args.dry_run:
        return 0

    IPROPS.write_text(source[:start] + rendered + "\n" + source[end:])
    json.loads(rendered)  # the file must still parse as what it claims to be
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
