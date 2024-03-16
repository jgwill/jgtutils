

import sys

import logging

import traceback

import logging
_loglevel = logging.WARNING
        

# Create a logger object
log = logging.getLogger(__name__)
log.setLevel(_loglevel)


# Create a console handler and set its level
console_handler = logging.StreamHandler()
console_handler.setLevel(_loglevel)

# Create a formatter and add it to the console handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

def set_log_level(loglevel: str = "WARNING"):
    global _loglevel,log,console_handler
    _loglevel = getattr(logging, loglevel)
    log.setLevel(_loglevel)
    console_handler.setLevel(_loglevel)
    log.info(f"Log level set to {_loglevel}")

def write_log(msg: str, loglevel: str = "INFO"):
    global _loglevel,log,console_handler
    loglevel = getattr(logging, loglevel)
    if loglevel >= _loglevel:
        log.log(loglevel, msg)

# try:
  

#   # Add the console handler to the logger
#   log.addHandler(console_handler)
# except Exception as e:
#   print("Exception: {0}\n{1}".format(e, traceback.format_exc()))
#   print('logging failed - dont worry')


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
    log=logging.getLogger(__name__).addHandler(console_handler)
except Exception as e:
    print("Exception: {0}\n{1}".format(e, traceback.format_exc()))
    print('logging failed - dont worry')
