


# Copyright 2019 Gehtsoft USA LLC
# Copyright 2023 JGWill (extended/variations)

# Licensed under the license derived from the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

# http://fxcodebase.com/licenses/open-source/license.html

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from enum import Enum
import json
import os
import tlid

#------------------------#

# common.py


#import logging
import datetime
import traceback
import argparse
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtos import tlid_range_to_start_end_datetime,tlid_range_to_jgtfxcon_start_end_str,tlid_dt_to_string,tlidmin_to_dt

try :
    import __main__
    # logging.basicConfig(filename='{0}.log'.format(__main__.__file__), level=logging.INFO,
    #                 format='%(asctime)s %(levelname)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
    # console = logging.StreamHandler(sys.stdout)
    # console.setLevel(logging.INFO)
    # logging.getLogger('').addHandler(console)
    

except:
    #print('logging failed - dont worry')
    pass

try :    
    #if __main__ has a .parser then set the default parser to that
    if hasattr(__main__,'parser'):
        default_parser=__main__.parser
    else:
        if hasattr(__main__,'default_parser'):
            default_parser=__main__.default_parser
        else: 
            if hasattr(__main__,'__parser__'):
                default_parser=__main__.__parser__
            else:
                default_parser = argparse.ArgumentParser(description='JGWill Trading Utilities')
except:
    default_parser = argparse.ArgumentParser(description='JGWill Trading Utilities')
    pass

def init_default_parser(description: str):
    global default_parser
    default_parser = argparse.ArgumentParser(description=description)
    return default_parser

def add_main_arguments(parser: argparse.ArgumentParser=None):
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('--login',
                        metavar="LOGIN",
                        required=True,
                        help='Your user name.')

    parser.add_argument('--password',
                        metavar="PASSWORD",
                        required=True,
                        help='Your password.')

    parser.add_argument('--urlserver',
                        metavar="URL",
                        required=True,
                        help='The server URL. For example,\
                                 https://www.fxcorporate.com/Hosts.jsp.')

    parser.add_argument('--connection',
                        metavar="CONNECTION",
                        required=True,
                        help='The connection name. For example, \
                                 "Demo" or "Real".')


    parser.add_argument('-session',
                        help='The database name. Required only for users who\
                                 have accounts in more than one database.\
                                 Optional parameter.')

    parser.add_argument('-pin',
                        help='Your pin code. Required only for users who have \
                                 a pin. Optional parameter.')
    return parser

def add_candle_open_price_mode_argument(parser: argparse.ArgumentParser=None):
    global default_parser
    if parser is None:
        parser=default_parser
    parser.add_argument('--openpricemode',
                        metavar="CANDLE_OPEN_PRICE_MODE",
                        default="prev_close",
                        help='Ability to set the open price candles mode. \
                        Possible values are first_tick, prev_close. For more information see description \
                        of O2GCandleOpenPriceMode enumeration. Optional parameter.')
    return parser

def add_instrument_timeframe_arguments(parser: argparse.ArgumentParser=None, timeframe: bool = True,add_IndicatorPattern=False):
    
    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-i','--instrument',
                        metavar="INSTRUMENT",
                        help='An instrument which you want to use in sample. \
                                  For example, "EUR/USD".')

    if timeframe:
        parser.add_argument('-t','--timeframe',
                            metavar="TIMEFRAME",
                            help='Time period which forms a single candle. \
                                      For example, m1 - for 1 minute, H1 - for 1 hour.')
    if add_IndicatorPattern:
        parser.add_argument('-ip',
                        metavar="IndicatorPattern",
                        required=False,
                        help='The indicator Pattern. For example, \
                                 "AOAC","JTL,"JTLAOAC","JTLAOAC","AOACMFI".')
    return parser
    

def add_direction_rate_lots_arguments(parser: argparse.ArgumentParser=None, direction: bool = True, rate: bool = True,
                                      lots: bool = True):
    global default_parser
    if parser is None:
        parser=default_parser

    if direction:
        parser.add_argument('-d', metavar="TYPE", required=True,
                            help='The order direction. Possible values are: B - buy, S - sell.')
    if rate:
        parser.add_argument('-r', metavar="RATE", required=True, type=float,
                            help='Desired price of an entry order.')
    if lots:
        parser.add_argument('-lots', metavar="LOTS", default=1, type=int,
                            help='Trade amount in lots.')
    
    return parser


def add_account_arguments(parser: argparse.ArgumentParser=None):
    global default_parser
    if parser is None:
        parser=default_parser
    parser.add_argument('-account', metavar="ACCOUNT",
                        help='An account which you want to use in sample.')
    return parser


def str_to_datetime(date_str):
    formats = ['%m.%d.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y/%m/%d', '%Y-%m-%d']
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def valid_datetime(check_future: bool):
    def _valid_datetime(str_datetime: str):
        date_format = '%m.%d.%Y %H:%M:%S'
        try:
            result = datetime.datetime.strptime(str_datetime, date_format).replace(
                tzinfo=datetime.timezone.utc)
            if check_future and result > datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc):
                msg = "'{0}' is in the future".format(str_datetime)
                raise argparse.ArgumentTypeError(msg)
            return result
        except ValueError:
            now = datetime.datetime.now()
            msg = "The date '{0}' is invalid. The valid data format is '{1}'. Example: '{2}'".format(
                str_datetime, date_format, now.strftime(date_format))
            raise argparse.ArgumentTypeError(msg)
    return _valid_datetime


def add_tlid_range_argument(parser: argparse.ArgumentParser=None):
    global default_parser
    if parser is None:
        parser=default_parser
    #print("Tlid range active")
    parser.add_argument('-r', '--range', type=str, required=False, dest='tlidrange',
                        help='TLID range in the format YYMMDDHHMM_YYMMDDHHMM.')
    return parser

def add_date_arguments(parser: argparse.ArgumentParser=None, date_from: bool = True, date_to: bool = True):
    global default_parser
    if parser is None:
        parser=default_parser
        
    if date_from:
        parser.add_argument('-s','--datefrom',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Date/time from which you want to receive\
                                      historical prices. If you leave this argument as it \
                                      is, it will mean from last trading day. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True)
                            )
    if date_to:
        parser.add_argument('-e','--dateto',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      historical prices. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(False)
        )
    return parser


def add_report_date_arguments(parser: argparse.ArgumentParser=None, date_from: bool = True, date_to: bool = True):
    global default_parser
    if parser is None:
        parser=default_parser
        
    if date_from:
        parser.add_argument('-s','--datefrom',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime from which you want to receive\
                                      combo account statement report. If you leave this argument as it \
                                      is, it will mean from last month. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True)
                            )
    if date_to:
        parser.add_argument('-e','--dateto',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      combo account statement report. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(True)
        )
    return parser


def add_max_bars_arguments(parser: argparse.ArgumentParser=None):
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('-c','--quotescount',
                        metavar="MAX",
                        default=-1,
                        type=int,
                        help='Max number of bars. 0 - Not limited')
    
    return parser


# def add_bars_arguments(parser: argparse.ArgumentParser=None):
    # global default_parser
    # if parser is None:
    #     parser=default_parser
#     parser.add_argument('-bars',
#                         metavar="COUNT",
#                         default=3,
#                         type=int,
#                         help='Build COUNT bars. Optional parameter.')


def add_output_argument(parser: argparse.ArgumentParser=None):
    """
    Adds an output argument to the given argument parser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to add the output argument to.

    Returns:
        parser (argparse.ArgumentParser): The argument parser with the output argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('-o','--output',
                        action='store_true',
                        help='Output PATH. If specified, output will be written in the filestore.')
    
    return parser

def add_compressed_argument(parser: argparse.ArgumentParser=None):
    """
    Adds an compressed argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the output argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('-z','--compress',
                        action='store_true',
                        help='Compress the output. If specified, it will also activate the output flag.')
    return parser


def add_use_full_argument(parser: argparse.ArgumentParser=None):
    """
    Adds a use full argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the read full argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('-uf','--full',
                        action='store_true',
                        help='Output/Input uses the full store. ')
    parser.add_argument('-un','--notfull',
                        action='store_true',
                        help='Output/Input uses NOT the full store. ')
 
    return parser

def add_use_fresh_argument(parser: argparse.ArgumentParser=None):
    """
    Adds a use fresh argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the use fresh argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    parser.add_argument('-new','--fresh',
                        action='store_true',
                        help='Output/Input freshes storage with latest market. ')
    parser.add_argument('-old','--notfresh',
                        action='store_true',
                        help='Output/Input wont be freshed from storage (weekend or tests). ')
 
    return parser


def add_keepbidask_argument(parser: argparse.ArgumentParser=None):
    """
    Adds a keep Bid/Ask argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the keep bid/ask argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with the argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
    parser.add_argument('-kba','--keepbidask',
                        action='store_true',
                        help='Keep Bid/Ask in storage. ')
    parser.add_argument('-rmba','--rmbidask',
                        action='store_true',
                        help='Remove Bid/Ask in storage. ')
    return parser

def add_exit_if_error(parser: argparse.ArgumentParser=None):
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('-xe','--exitonerror',
                        action='store_true',
                        help='Exit on error rather than trying to keep looking')
    return parser

def add_viewpath_argument(parser: argparse.ArgumentParser=None):
    """
    Adds an view path argument to the given argument parser.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser to add the viewpath argument to.
        
    Returns:
        parser (argparse.ArgumentParser): The argument parser with the argument added.
    """
    global default_parser
    if parser is None:
        parser=default_parser
        
    parser.add_argument('-vp','--viewpath',
                        action='store_true',
                        dest='viewpath',
                        help='flag to just view the path of files from arguments -i -t.')
    return parser


# def add_quiet_argument(parser: argparse.ArgumentParser=None):
#     parser.add_argument('-q','--quiet',
#                         action='store_true',
#                         help='Suppress all output. If specified, no output will be printed to the console.')
#     return parser

def add_verbose_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=0,
                        help='Set the verbosity level. 0 = quiet, 1 = normal, 2 = verbose, 3 = very verbose, etc.')
    return parser

def add_cds_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-cds','--cds',
                        action='store_true',
                        default=False,
                        help='Action the creation of CDS')
    return parser

def add_ids_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-ids','--ids',
                        action='store_true',
                        default=False,
                        help='Action the creation of IDS')
    return parser


def add_ids_mfi_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser
    parser.add_argument(
        "-mfi",
        "--mfi_flag",
        action="store_true",
        help="Enable the Market Facilitation Index indicator.",
    )
    parser.add_argument(
        "-nomfi",
        "--no_mfi_flag",  
        action="store_true",
        help="Disable the Market Facilitation Index indicator.",
    )  
    return parser

def add_ids_gator_oscillator_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument(
        "-go",
        "--gator_oscillator_flag",
        action="store_true",
        help="Enable the Gator Oscillator indicator.",
    )
    return parser

def add_ids_fractal_largest_period_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument(
        "-lfp",
        "--largest_fractal_period",
        type=int,
        default=89,
        help="The largest fractal period.",
    )
    return parser

def add_ids_balligator_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser
    
    parser.add_argument(
        "-ba",
        "--balligator_flag",
        action="store_true",
        help="Enable the Big Alligator indicator.",
    )
    parser.add_argument(
        "-bjaw",
        "--balligator_period_jaws",
        type=int,
        default=89,
        help="The period of the Big Alligator jaws.",
    )
    return parser
  
def add_ids_talligator_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser
    
    parser.add_argument(
        "-ta",
        "--talligator_flag",
        action="store_true",
        help="Enable the Tide Alligator indicator.",
    )
    parser.add_argument(
        "-tjaw",
        "--talligator_period_jaws",
        type=int,
        default=377,
        help="The period of the Tide Alligator jaws.",
    )
    return parser

def add_ads_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-ads','--ads',
                        action='store_true',
                        default=False,
                        help='Action the creation of ADS and show the chart')
    return parser

def add_iprop_init_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-iprop','--iprop',
                        action='store_true',
                        default=False,
                        help='Toggle the downloads of all instrument properties ')
    return parser

def add_debug_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-debug','--debug',
                        action='store_true',
                        default=False,
                        help='Toggle debug ')
    return parser

def add_pdsserver_argument(parser: argparse.ArgumentParser=None):

    global default_parser
    if parser is None:
        parser=default_parser

    parser.add_argument('-server','--server',
                        action='store_true',
                        default=False,
                        help='Run the server ')
    return parser


def print_exception(exception: Exception):
    #logging.error("Exception: {0}\n{1}".format(exception, traceback.format_exc()))
    print("Exception: {0}\n{1}".format(exception, traceback.format_exc()))






def diff_month(year: int, month: int, date2: datetime):
    return (year - date2.year) * 12 + month - date2.month



def export_env_if_any(config):
    # if has a key : "keep_bid_ask" and if yes and set to "true", export an env variable "JGT_KEEP_BID_ASK" to "1"
    if 'keep_bid_ask' in config and config['keep_bid_ask'] == True:
        os.environ['JGT_KEEP_BID_ASK'] = '1'

_JGT_CONFIG_JSON_SECRET=None

def readconfig(json_config_str=None,config_file = 'config.json',export_env=False,config_file_path_env_name='JGT_CONFIG_PATH',config_values_env_name='JGT_CONFIG'):
    global _JGT_CONFIG_JSON_SECRET
    #print argument values to debug
    _DEBUG_240619=False
    if _DEBUG_240619:
        print("json_config_str:",json_config_str)
        print("config_file:",config_file)
        print("export_env:",export_env)
        print("config_file_path_env_name:",config_file_path_env_name)
        print("config_values_env_name:",config_values_env_name)
    
    # Try reading config file from current directory

    if json_config_str is not None:
        config = json.loads(json_config_str)
        _JGT_CONFIG_JSON_SECRET=json_config_str
        if export_env:
            export_env_if_any(config)
        return config
    
    
    if _JGT_CONFIG_JSON_SECRET is not None:
        config = json.loads(_JGT_CONFIG_JSON_SECRET)
        if export_env:
            export_env_if_any(config)
        return config
    
    config = None

    # if file does not exist try set the path to the file in the HOME
    if not os.path.exists(config_file):
        config_file = os.path.join(os.path.expanduser("~"), config_file)
        
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            if export_env:
                export_env_if_any(config)
            return config
    else:
        # If config file not found, check home directory
        home_dir = os.path.expanduser("~")
        config_file = os.path.join(home_dir, config_file)
        if os.path.isfile(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            # If config file still not found, try reading from environment variable
            config_json_str = os.getenv('JGT_CONFIG_JSON_SECRET')
            if config_json_str:
                config = json.loads(config_json_str)
                if export_env:
                    export_env_if_any(config)
                return config


    # Now you can use the config dictionary in your application

    # if file dont exist, try loading from env var JGT_CONFIG
    if not os.path.exists(config_file):
        config_json_str = os.getenv(config_values_env_name)
        
        if config_json_str:
            config = json.loads(config_json_str)
            if export_env:
                export_env_if_any(config)
            #return config
        else:
            # if not found, try loading from env var JGT_CONFIG_PATH
            config_file = os.getenv(config_file_path_env_name)
            if config_file:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if export_env:
                        export_env_if_any(config)
                    #return config
           # else:
               
    # Read config file
    if config is None:
        print("config_file:",config_file)
        if config_file is not None and os.path.exists(config_file) :
            with open(config_file, 'r') as file:
                config = json.load(file)
        
    if config is None:
        raise Exception(f"Configuration not found. Please provide a config file or set the JGT_CONFIG environment variable to the JSON config string. (config_file={config_file})")
    
    if export_env:
        export_env_if_any(config)
    return config
