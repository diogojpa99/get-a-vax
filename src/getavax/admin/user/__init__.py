
import uuid
from datetime import date, datetime

from pyramid.view import view_config

from ..time import Interval

def includeme(config):
  config.add_route('admin.user.generate_schedule', '/user/generate-schedule')
  return

class Rules:
  def __init__(self, agemin, agemax, period, fixed_intervals, ):
    self.agemin = agemin
    self.agemax = agemax
    self.period = period
    self.fixed_intervals = fixed_intervals
    return

  def next(self, born_at, at, last):
    #age_in_days = (at.year - born_at.year) * 365
    # Consider leap years
    age_in_days = (at - born_at).days
    
    if self.agemin.isvalid():
      min_days = self.agemin.days()
      if age_in_days < min_days:
        return None
      
    if self.agemax.isvalid():
      max_days = self.agemax.days()
      if age_in_days > max_days:
        return None
      
    if self.period.isvalid():
      if last is None:
          return at
      else:
        n = last + self.period.timedelta()
        return at if n < at else n
      
    else:
      for i in self.fixed_intervals:
        n = born_at + i
        if n > at:
          return n
      return None

  @staticmethod
  def ofrow(row):
    agemin = Interval(row['agemin_value'], row['agemin_unit'])
    agemax = Interval(row['agemax_value'], row['agemax_unit'])
    period = None
    fixed_intervals = []
    if row['value']:
      period = Interval(row['value'], row['unit'])
    else:
      names = (('value'+str(i), 'unit'+str(i)) for i in range(1,10))
      fixed_intervals = [Interval(row[name[0]], row[name[1]]) for name in names if row[name[1]] ]
    return Rules(agemin, agemax, period, fixed_intervals)


@view_config(route_name='admin.user.generate_schedule', renderer='json')
def gen(request):
  at = get_key(request.POST, 'at', date.today, date.fromisoformat)
  id_user_ers = get_key(request.POST, 'id_user_ers', map_fn=uuid.UUID)
  if id_user_ers is None:
    raise Exception('no user')

  rvalue = {}
  sql = """SELECT
  v2u.*, v.*, vra.*, vrb.*,
  (SELECT born_at from user_ers where id_user_ers=v2u.id_user_ers) born_at
  FROM
    vaccine v
    INNER JOIN vaccine_rules_age vra ON vra.id_vaccine = v.id_vaccine
    INNER JOIN vaccine_rules_booster vrb ON vrb.id_vaccine = v.id_vaccine
    INNER JOIN vaccine_user_configuration v2u ON v.id_vaccine = v2u.id_vaccine AND v2u.enabled
  WHERE v2u.id_user_ers=%s
"""
  db = request.environ['db']
  db.execute(sql, (id_user_ers,))
  rows = db.fetchall()

  user_vcount = 0
  to_process = []
  to_insert = []
  sql = """SELECT DISTINCT id_vaccine
  FROM vaccine_user_schedule_event vce
  WHERE id_user_ers=%s {other_predicates}
  """
  for r in rows:
    user_vcount += 1
    id_vaccine = r['id_vaccine']
    born_at = r['born_at']
    last_shot_at = get_key(r, 'last_shot_at', date.fromisoformat)
    rules = Rules.ofrow(r)
    next_shot_at = rules.next(born_at, at, last_shot_at)
    if next_shot_at is None or next_shot_at < at:
      continue
    to_process.append((id_vaccine, next_shot_at))

  tmpsql = ""
  for i in to_process:
    tmpsql += " AND (id_vaccine=%s AND reference_date=%s)"
  sql = sql.format(other_predicates=tmpsql)

  db.execute(sql, (id_user_ers, *(i for t in to_process for i in t)))
  rows = set((row['id_vaccine'] for row in db.fetchall()))
  for id_vaccine, next_shot_at in to_process:
    if not id_vaccine in rows:
      id_vaccine_schedule_event = uuid.uuid4()
      to_insert.append((id_vaccine_schedule_event, id_user_ers, id_vaccine, next_shot_at, ))
  rvalue['user_vaccine_count'] = user_vcount
  rvalue['generated'] = len(to_insert)

  if to_insert:
    sql = """INSERT INTO vaccine_user_schedule_event
    (id_vaccine_user_schedule_event, id_user_ers, id_vaccine, reference_date, created_at, audit_data)
    VALUES (%s,%s,%s,%s,%s,%s)"""
    for t in to_insert:
      now = datetime.now()
      audit_data = {}
      db.execute(sql, (*t, now, audit_data))
  return rvalue


def identity(x): return x
def none(): return
def get_key(bag, key, default_value_fn=none, map_fn = identity):
  return map_fn(bag[key]) if key in bag else default_value_fn()

# vim: set et ts=2 sw=2  : 
