

import datetime
import json, urllib
import queue,threading
from getavax.db import cursor

__q__ = None
__ers_baseurl__ = None
__availability__ = 0

def get():
  return __availability__

def work():
  import datetime
  global __q__
  while True:
    try:
      __q__.get(timeout=60);
      f = datetime.datetime.now()
      t = f + datetime.timedelta(hours=7)
      update_availability(f, t)
    except queue.Empty:
      f = datetime.datetime.now()
      t = f + datetime.timedelta(hours=7)
      update_availability(f, t)
      continue
  return

def put(arg, /):
    __q__.put((None, arg))

def includeme(config):
  global __ers_baseurl__
  __ers_baseurl__ = config.get_settings().get('ersapi.baseurl',
              'http://web-ersapi.int.ace.premium-minds.com:8081')

  global __q__
  if __q__:
    print("error")
  else:
    __q__ = queue.Queue()
    print("starting off")
    threading.Thread(target=work).start()
  return

def update_availability(f, t, ):
  data = {}
  with cursor() as db:
    db.execute('SELECT c.* from clinic c')
    for r in db:
      tmp = do_fetch_availability(r['id_clinic'], f, t)
      for (ts, count) in tmp['disponibilidade']:
        data[ts] = data.get(ts, 0) + count
  global __availability__
  __availability__ = sum(data.values())
  return


def do_fetch_availability(clinic, _from, to):
  params = {'desde': _from.isoformat(), 'a': to.isoformat(' '), 'centro': clinic }
  url = urllib.parse.urljoin(__ers_baseurl__, '/disponibilidade?' + urllib.parse.urlencode(params))
  with urllib.request.urlopen(url) as f:
    rvalue = json.load(f)
  return rvalue

# vim: set et ts=2 sw=2  : 
