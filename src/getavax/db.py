
from contextlib import contextmanager

import logging

import psycopg2
import psycopg2.extras
import psycopg2.extensions

from psycopg2.extras import DictCursor #, LoggingCursor, LoggingConnection

__db__ = {}
__log__ = logging.getLogger(__name__)
__conn__ = None

#class MyCursor(DictCursor, LoggingCursor):
#  pass

def tween_factory(h, r):
  if not __db__:
    __log__.warn('database configuration missing')
    return
  psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
  psycopg2.extras.register_uuid()
  def _h(req):
    conn = psycopg2.connect(**__db__)
    #conn = psycopg2.connect(connection_factory=LoggingConnection, **__db__)
    conn.set_session(autocommit=False)
    #conn.initialize(__log__)
    cur = conn.cursor(cursor_factory=DictCursor)
    req.environ['db'] = cur
    try:
      rsp = h(req)
      return rsp
    finally:
      cur.close()
      conn.close()
  return _h

@contextmanager
def cursor():
  conn = psycopg2.connect(**__db__)
  conn.set_session(autocommit=False)
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  try:
    yield cur
  finally:
    cur.close()
    conn.close()

def setparams(name, host, user, password):
  __db__['dbname'] = name
  __db__['host'] = host
  __db__['user'] = user
  __db__['password'] = password
  return


# vi: set ts=2 sw=2 et : 
