import os



from datetime import datetime, timedelta

from dateutil.parser import parse



def calculate_start_datetime(end_datetime, timeframe, periods):
  # Parse end_datetime string into datetime object
  end_datetime = parse(end_datetime)
  
  # Check if timeframe is in hours
  if timeframe.startswith('H'):
    # Convert timeframe from hours to minutes
    timeframe_minutes = int(timeframe[1:]) * 60
  elif timeframe.startswith('D'):
    # Convert timeframe from days to minutes
    timeframe_minutes = int(timeframe[1:]) * 24 * 60
  else:
    # Assume timeframe is already in minutes
    timeframe_minutes = int(timeframe)
  
  # Convert timeframe from minutes to seconds
  timeframe_seconds = timeframe_minutes * 60
  # Calculate total seconds for all periods
  total_seconds = timeframe_seconds * periods
  # Calculate start datetime
  start_datetime = end_datetime - timedelta(seconds=total_seconds)
  return start_datetime