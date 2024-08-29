import datetime
import time
import os

import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgtcommon

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

def parse_args():
    parser = jgtcommon.new_parser("JGT Cron Test","Test launching or unlocking (exit when specific timeframes arrives.)",enable_specified_settings=True)
    #parser=jgtcommon.add_settings_argument(parser)
    #parser=jgtcommon._preload_settings_from_args(parser)
    
    parser= jgtcommon.add_timeframe_standalone_argument(parser,required=True)
    #exit the program when the timeframe is reached
    parser.add_argument("-X", "--exit", action="store_true", help="Exit the program when the timeframe is reached.")
    #parser=jgtcommon.add_bars_amount_V2_arguments(parser)
    #parser=jgtcommon.add_keepbidask_argument(parser)
    #parser=jgtcommon.add_tlid_range_argument(parser)
    parser=jgtcommon.add_verbose_argument(parser)
    
    args = jgtcommon.parse_args(parser)
    return args

def main():
    args = parse_args()
    ctx_times = get_times_by_timeframe_str(args.timeframe)
    print(f"CTX times: {ctx_times}")
    sleep_duration = 60 if args.timeframe != "m1" else 2
    
    while True:
      current_time = datetime.datetime.now().strftime("%H:%M") if args.timeframe != "m1" else datetime.datetime.now().strftime("%H:%M:%S")
      # H4 = ["01:00", "05:00", "9:00", "13:00","17:00","21:00"]
      # H1=["00:00","01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
      # m15=["00:00","00:15","00:30","00:45","01:00", "01:15", "01:30", "01:45", "02:00", "02:15", "02:30", "02:45", "03:00", "03:15", "03:30", "03:45", "04:00", "04:15", "04:30", "04:45", "05:00", "05:15", "05:30", "05:45", "06:00", "06:15", "06:30", "06:45", "07:00", "07:15", "07:30", "07:45", "08:00", "08:15", "08:30", "08:45", "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45", "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "20:00", "20:15", "20:30", "20:45", "21:00", "21:15", "21:30", "21:45", "22:00", "22:15", "22:30", "22:45", "23:00", "23:15", "23:30", "23:45"]
      # m15b=get_timeframes_times_by_minutes(15)
      # m5=get_timeframes_times_by_minutes(5)
      
      if current_time in ctx_times:  # Adjust the times as needed
          if args.exit:
              print("Exiting to do what is next")
              exit(0)
          output = refreshTF(args.timeframe)
          print(output)
          time.sleep(sleep_duration)  # Sleep for 60 seconds to avoid multiple runs within the same minute
      time.sleep(1)  # Check every second
      #print(".", end="")
    sys.stdout.flush()

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
    
