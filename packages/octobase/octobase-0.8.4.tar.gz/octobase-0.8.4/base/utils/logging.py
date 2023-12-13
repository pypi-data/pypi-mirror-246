#!/opt/local/bin/python
''' Helpers for logging to console. '''

import base
import datetime
import logging
import logging.handlers
import os
import sys
import traceback


class TimeFormatFilter(logging.Filter):
  ''' adds a `%(isotime)s` field to the log record '''

  def filter(self, record):
    timestamp       = datetime.datetime.fromtimestamp(record.created)
    timezoned       = base.utils.LocalTime(base.utils.EnsureTzInfo(timestamp))
    record.isotime  = timezoned.isoformat()
    return True


def ConfigureLogging(filepath=None):
  if filepath:
    dirpath       = os.path.dirname(filepath)
    if dirpath and not os.path.exists(dirpath):
      os.makedirs(dirpath, exist_ok=True)

  filter          = TimeFormatFilter()
  simplex         = logging.Formatter('%(name)s %(message)s')
  complex         = logging.Formatter('%(isotime)s %(name)s %(message)s')

  console         = logging.StreamHandler()
  console.setLevel(logging.INFO)
  console.setFormatter(simplex)
  console.addFilter(filter)

  if filepath:
    logfile       = logging.handlers.WatchedFileHandler(filepath, delay=True)
    logfile.setLevel(logging.INFO)
    logfile.setFormatter(complex)
    logfile.addFilter(filter)


  logger          = logging.getLogger()
  logger.setLevel(logging.INFO)
  if filepath:
    logger.addHandler(logfile)
  logger.addHandler(console)



_USE_LOGGING      = None

def Log(tag, message, level=logging.INFO, **extra):
  ''' Logs a message.  The "tag" should be a sluglike label for the type of log message. '''
  tag             = tag and base.utils.Slugify(tag).upper() or None
  if level != logging.INFO:
    tag           = (tag and (tag + '.') or '') + logging.getLevelName(level)

  global _USE_LOGGING
  if _USE_LOGGING is None:
    _USE_LOGGING  = False
    logger        = logging.getLogger(tag)
    while logger:
      if logger.handlers:
        _USE_LOGGING  = True
        break
      logger      = logger.parent

  if _USE_LOGGING:
    logging.getLogger(tag).log(level, message or '', extra=extra)
  else:
    things        = [x for x in (tag, message) if x]
    sys.stderr.write(' '.join(things) + '\n')



def LogTraceback(error=None, limit=12):
  ''' Logs a stack trace to the console. '''
  exc_type, exc_value, exc_traceback = error and sys.exc_info() or (None, None, None)
  limit           += 1
  raw             = exc_traceback and traceback.extract_tb(exc_traceback, limit=limit) or traceback.extract_stack(limit=limit)
  lines           = traceback.format_list(raw)
  if lines and not exc_traceback:
    lines         = lines[:-1]
  if lines:
    Log('TRACEBACK', '\n' + '\n'.join(lines))


def LogException(exception):
  ''' Logs an exception to the console. '''
  last            = traceback.extract_tb(exception.__traceback__)[-1]
  filename        = last.filename
  text            = str(exception).replace('\n', '\n . ')
  base.utils.Log(
      'EXCEPTION', '{filename}:{lineno}\n - {line}\n - {text}'.format(
          filename=filename, lineno=last.lineno, line=last.line, name=last.name, text=text),
      level=logging.WARN)


def XYZZY(*messages):
  ''' Logs a debug message to the console.

      The function name "XYZZY" is chosen to be easy to search for in a codebase,
      to help reduce debug code being committed into production.
  '''
  if not messages:
    Log('XYZZY', None)
  elif len(messages) == 1:
    Log('XYZZY', repr(messages[0]))
  else:
    message       = ''
    for i in range(len(messages)):
      message     = message + '\n {:2d}: '.format(i) + repr(messages[i]).rstrip()
    Log('XYZZY', message)
