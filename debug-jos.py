# %%  
import jgtutils.jgtos as jos
import os


i = "EUR/USD"
t = "H4"
tlid_range = "231010_240105"



actual=jos.create_filestore_path(
    i,
    t,
    quiet=False,
    compressed=False,
    tlid_range=tlid_range,
    output_path="/data",
    nsdir="pds",
)

expected='/data/pds/EUR-USD_H4_2310100000_2401052359.csv'

print(f"actual={actual} expected={expected}")
if actual==expected:
    print("PASS")
else:
    print("FAIL")
# %%
