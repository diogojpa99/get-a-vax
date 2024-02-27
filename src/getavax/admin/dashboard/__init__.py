
import datetime
import json
import urllib

from pyramid.view import view_config

from ..page.menu import menu_entries

__dashboard__ = {
    'updated_at': datetime.datetime(1, 1, 1),
    'vagas' : 0,
    'agendamentos': -1,
}

def includeme(config):
  config.add_route('admin.dashboard', '/')
  config.add_route('admin.dashboard.data.get', '/dashboard/data.json')
  from . import availability
  availability.includeme(config)
  return

@view_config(route_name='admin.dashboard', renderer='dashboard.mako')
def admin_dashboard(request):
  rvalue = {
      'project': 'GET-A-VAX',
      'title': 'Dashboard',
      'menu_entries': menu_entries(),
      'dashboard': None,
  }
  at = request.params.get('at')
  delta = int(request.params.get('delta', 7))
  f = datetime.datetime.fromisoformat(at.replace('Z','')) if at else datetime.datetime.now()
  t = f.replace(hour=(f.hour+delta) % 24)
  db = request.environ['db']
  do_run_dashboard(db, f, t)
  rvalue['at'] = at
  rvalue['delta'] = delta
  rvalue['dashboard'] = __dashboard__
  return rvalue

@view_config(route_name='admin.dashboard.data.get', renderer='json')
def getdata(request):
  at = request.params.get('at')
  delta = int(request.params.get('delta', 7))
  f = datetime.datetime.fromisoformat(at.replace('Z','')) if at else datetime.datetime.now()
  t = f.replace(hour=(f.hour+delta) % 24)
  if (f - __dashboard__['updated_at']).seconds > 30:
    db = request.environ['db']
    do_run_dashboard(db, f, t)
  rvalue = {'at': at, 'delta': delta}
  rvalue.update(__dashboard__)
  return rvalue

def do_run_dashboard(db, f,t):
  global __dashboard__
  data = {}
  ff = f.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  sql = '''WITH data AS (
      SELECT id_clinic, id_vaccine, count(*) c
      FROM vaccine_user_schedule_event_scheduled se
      INNER JOIN vaccine_user_schedule_event e ON e.id_vaccine_user_schedule_event = se.id_vaccine_user_schedule_event
      WHERE %s <= se.s_at_date and se.s_at_date <= %s
      GROUP BY id_clinic, id_vaccine
    )
    SELECT data.*,c.name cname,v.name vname
    FROM data
     INNER JOIN clinic c ON c.id_clinic=data.id_clinic
     INNER JOIN vaccine v ON v.id_vaccine=data.id_vaccine
    ORDER BY c DESC, v.name ASC, c.name DESC
    LIMIT 10'''
  db.execute(sql, (ff, f))
  rows = db.fetchall()
  maxcount=rows[0]['c'] if rows else 1
  mincount=rows[-1]['c'] if rows else 0
  data['top'] = { 'from': ff, 'to': f, 'data': [(x['vname'], x['cname'], x['c'], x['c'] / maxcount * 100, mincount, maxcount) for x in rows] }

  from . import availability
  availability.update_availability(f, t)
  data['vagas'] = availability.get()

  db.execute('''SELECT COUNT(*) cnt
    FROM vaccine_user_schedule_event_scheduled
    WHERE %s <= s_at_date AND s_at_date <= %s''', (f, t))
  r = db.fetchone()

  data['agendamentos'] = r['cnt']
  __dashboard__.update(data)
  return



# vi: set ts=2 sw=2 et : 
