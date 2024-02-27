
from getavax.db import cursor

__ers_baseurl__ = None

def includeme(config):
  global __ers_baseurl__
  __ers_baseurl__ = config.get_settings()['ersapi.baseurl']
  return

def fetch_clinic(c, f, t, now):
  sql = '''
    DELETE FROM clinic_availability_cache
      WHERE cache_valid_to <= %s and id_clinic = %s
  '''

  sql = '''
  SELECT cac.* FROM clinic_availability_cache cac
  WHERE TRUE
     AND id_clinic=%s
     AND %s <= timeslot AND timeslot <= %s
  '''
  rvalue = {}
  with cursor() as cur:
    cur.execute(sql, (c, f, t))
    rvalue['disponibilidade'] = [x for x in cur]
  print(rvalue)


  return 



# vim: set et ts=2 sw=2  : 
