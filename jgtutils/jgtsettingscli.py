import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon

def parse_args():
    parser = jgtcommon.new_parser("JGTFxCLI Settings Loader", "Load and output settings as JSON", enable_specified_settings=True)
    parser=jgtcommon.add_settings_argument(parser)
    # parser = jgtcommon.add_instrument_timeframe_arguments(parser)
    # parser = jgtcommon.add_bars_amount_V2_arguments(parser)
    # parser = jgtcommon.add_keepbidask_argument(parser)
    # parser = jgtcommon.add_tlid_range_argument(parser)
    # parser = jgtcommon.add_verbose_argument(parser)
    args = jgtcommon.parse_args(parser)
    return args

def main():
    args = parse_args()
    settings = jgtcommon.load_settings()
    print("Settings loaded:")
    print(json.dumps(settings, indent=4))

if __name__ == '__main__':
    main()