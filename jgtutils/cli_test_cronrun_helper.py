import datetime
import time
import os

import sys


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon
from jgtclihelper import print_jsonl_message

import jgtwslhelper as wsl


def refreshTF( timeframe:str,quote_count:int=-1, quiet:bool=True,use_full:bool=False,verbose_level=0,tlid_range=None,keep_bid_ask=False):
  #if not quiet:
  print(f"Refreshing  {timeframe}")
  try:
    print("WE Would be processing our stuff: " + str(datetime.datetime.now()))
    #wsl.getPH(instrument, timeframe,quote_count=quote_count, tlid_range=tlid_range, use_full=use_full,verbose_level=verbose_level,keep_bid_ask=keep_bid_ask)
    return timeframe
  except Exception as e:
    print("Error in refreshPH")
    raise e

timeframe=None
from jgtclihelper import build_jsonl_message
def _exit_quietly_handler():
  global timeframe
  msg = f"Wait canceled by user"
  o=build_jsonl_message(msg,extra_dict={"timeframe":timeframe},state="canceled",scope=APP_SCOPE,use_short=True)
  return o

def parse_args():
    parser = jgtcommon.new_parser("JGT Cron Test","Test launching or unlocking (exit when specific timeframes arrives.)",enable_specified_settings=True,exiting_quietly_handler=_exit_quietly_handler)#add_exiting_quietly_flag=True,exiting_quietly_message=f"")
    #parser=jgtcommon.add_settings_argument(parser)
    #parser=jgtcommon._preload_settings_from_args(parser)
    
    parser= jgtcommon.add_timeframe_standalone_argument(parser,required=True)
    #exit the program when the timeframe is reached
    parser.add_argument("-X", "--exit", action="store_true", help="Exit the program when the timeframe is reached.")
    #--message
    parser.add_argument("-M", "--message", help="Message to display when the timeframe is reached.",default="Timeframe reached.")
    
    parser.add_argument("-I", "--in-message", help="Message to display when the timeframe wait starts.",default="Timeframe waiting started")
    
    #--nooutput
    parser.add_argument("-N", "--no-output", action="store_true", help="Do not output anything.")
    #parser=jgtcommon.add_bars_amount_V2_arguments(parser)
    #parser=jgtcommon.add_keepbidask_argument(parser)
    #parser=jgtcommon.add_tlid_range_argument(parser)
    parser=jgtcommon.add_verbose_argument(parser)
    
    args = jgtcommon.parse_args(parser)
    return args
APP_SCOPE="tfwait"
def main():
    global timeframe
    #add_exiting_quietly()
    
    args = parse_args()
    timeframe = args.timeframe
    
    ctx_times = get_times_by_timeframe_str(timeframe)
    quiet = args.quiet
    if not quiet:
      print(f"CTX times: {ctx_times}")
    sleep_duration = 60 if timeframe != "m1" else 2
    

    if not args.no_output:
      _print_app_message(timeframe,args.in_message,state="started" )
    while True:
      current_time = get_current_time(timeframe)
     
      
      if current_time in ctx_times:  # Adjust the times as needed
          if args.exit:
              #print(args.message," ",args.timeframe," reached at ",current_time)
              if not args.no_output:
                _print_app_message(timeframe, args.message,state="reached")
              #sys.stdout.flush()
              exit(0)
          output = refreshTF(args.timeframe)
          print(output)
          time.sleep(sleep_duration)  # Sleep for 60 seconds to avoid multiple runs within the same minute
      time.sleep(1)  # Check every second
      #print(".", end="")

def _print_app_message(timeframe, msg,state=None,use_short=True):
    print_jsonl_message(msg,extra_dict={"timeframe":timeframe,"time":get_current_time(timeframe)},scope=APP_SCOPE,state=state,use_short=use_short)

def get_current_time(timeframe):
    return datetime.datetime.now().strftime("%H:%M") if timeframe != "m1" else datetime.datetime.now().strftime("%H:%M:%S")

def get_times_by_timeframe_str(timeframe:str):
  if timeframe=="D1" or timeframe=="W1" or timeframe=="M1":
    return get_timeframe_daily_ending_time()
  if timeframe=="H8":
    return get_timeframes_times_by_minutes(8*60)
  if timeframe=="H4":
    return get_timeframes_times_by_minutes(4*60)
  if timeframe=="H3":
    return get_timeframes_times_by_minutes(3*60)
  if timeframe=="H2":
    return get_timeframes_times_by_minutes(2*60)
  if timeframe=="H1":
    return get_timeframes_times_by_minutes(60)
  if timeframe=="m30":
    return get_timeframes_times_by_minutes(30)
  if timeframe=="m15":
    return get_timeframes_times_by_minutes(15)
  if timeframe=="m5":
    return get_timeframes_times_by_minutes(5)
  if timeframe=="m1":
    return get_timeframes_times_by_minutes(1)

def get_timeframes_times_by_minutes(minutes:int):
    start_range = 0
    if minutes>=60:
        start_range = 1 # we start at 1:00 for those timeframes
    if minutes>1:
      return [f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(start_range,24) for m in range(0,60,minutes)]
    elif minutes==1:
      return [f"{str(h).zfill(2)}:{str(m).zfill(2)}:00" for h in range(start_range,24) for m in range(0,60) ] +  [f"{str(h).zfill(2)}:{str(m).zfill(2)}:01" for h in range(start_range,24) for m in range(0,60) ] # We are sure to process m1 at the end of the minute if by any chance we are late of 1 second

def get_timeframe_daily_ending_time() -> str:
    #if timeframe != "D1":
    #    raise ValueError("This function only handles the D1 timeframe.")
    
    now = datetime.datetime.now()
    year = now.year
    
    # Assuming DST starts on the second Sunday in March and ends on the first Sunday in November
    dst_start = datetime.datetime(year, 3, 8) + datetime.timedelta(days=(6 - datetime.datetime(year, 3, 8).weekday()))
    dst_end = datetime.datetime(year, 11, 1) + datetime.timedelta(days=(6 - datetime.datetime(year, 11, 1).weekday()))
    
    if dst_start <= now < dst_end:
        return "22:00:00"
    else:
        return "21:00:00"



if __name__ == '__main__':
    main()
    
