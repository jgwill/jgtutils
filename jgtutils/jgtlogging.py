

import sys

import logging

import traceback


import logging

_loglevel = logging.WARNING


_logger_name = __name__


def _proto():    
  global _loglevel,logger,console_handler
  try:
    log_file = __main__.__file__
  except:
    log_file = 'jgt'

  try :
      import __main__
      logging.basicConfig(filename='{0}.log'.format(log_file), level=logging.INFO,
                      format='%(asctime)s %(levelname)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
      console_handler = logging.StreamHandler(sys.stdout)
      console_handler.setLevel(_loglevel)
      logging.getLogger(_logger_name).addHandler(console_handler)
      return logger
  except Exception as e:
      print("Exception: {0}\n{1}".format(e, traceback.format_exc()))
      print('logging failed - dont worry')

_proto()


# %%
logger=logging.getLogger(_logger_name)
# Create a logger object
#log = logging.getLogger("jgt.log")
logger.setLevel(_loglevel)



# # Create a console handler and set its level
# console_handler = logging.StreamHandler()
# console_handler.setLevel(_loglevel)

# # Create a formatter and add it to the console handler
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)

def set_log_level(loglevel: str = "WARNING",logger_name = ""):
  global _loglevel,_logger_name,logger
  if logger_name == "":
    logger_name = _logger_name
  _loglevel = getattr(logging, loglevel)
  logging.getLogger(logger_name).setLevel(_loglevel)
  #console_handler.setLevel(_loglevel)
  logger.info(f"Log level set to {_loglevel}")

def write_log(msg: str, loglevel: str = "INFO"):
    global _loglevel,logger
    loglevel = getattr(logging, loglevel)
    if loglevel >= _loglevel:
        logging.log(loglevel, msg)
def info(msg: str):
  write_log(msg,"INFO")
def warning(msg: str):
  write_log(msg,"WARNING")
def error(msg: str):
  write_log(msg,"ERROR")
import logging
_loglevel = logging.WARNING
_loglevel = logging.DEBUG

_logger_name = __name__


def _proto():    
  global _loglevel,logger,console_handler
  try:
    log_file = __main__.__file__
  except:
    log_file = 'jgt'

  try :
      import __main__
      logging.basicConfig(filename='{0}.log'.format(log_file), level=logging.INFO,
                      format='%(asctime)s %(levelname)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
      console_handler = logging.StreamHandler(sys.stdout)
      console_handler.setLevel(_loglevel)
      logging.getLogger(_logger_name).addHandler(console_handler)
      return logger
  except Exception as e:
      print("Exception: {0}\n{1}".format(e, traceback.format_exc()))
      print('logging failed - dont worry')

_proto()


# %%
logger=logging.getLogger(_logger_name)
# Create a logger object
#log = logging.getLogger("jgt.log")
logger.setLevel(_loglevel)



# # Create a console handler and set its level
# console_handler = logging.StreamHandler()
# console_handler.setLevel(_loglevel)

# # Create a formatter and add it to the console handler
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)

def set_log_level(loglevel: str = "WARNING",logger_name = ""):
  global _loglevel,_logger_name,logger
  if logger_name == "":
    logger_name = _logger_name
  _loglevel = getattr(logging, loglevel)
  logging.getLogger(logger_name).setLevel(_loglevel)
  #console_handler.setLevel(_loglevel)
  logger.info(f"Log level set to {_loglevel}")

def write_log(msg: str, loglevel: str = "INFO"):
    global _loglevel,logger
    loglevel = getattr(logging, loglevel)
    if loglevel >= _loglevel:
        logging.log(loglevel, msg)
def info(msg: str):
  write_log(msg,"INFO")
def warning(msg: str):
  write_log(msg,"WARNING")
def error(msg: str):
  write_log(msg,"ERROR")
def critical(msg: str):
  write_log(msg,"CRITICAL")
def debug(msg: str):
  write_log(msg,"DEBUG")
  
