import json
import uuid

from dataclasses import dataclass
from datetime import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


from ..page.menu import menu_entries
from ..page.notification import Notification

def includeme(config):
  config.add_route('admin.scheduling.list', '/scheduling')
  return


@view_config(route_name='admin.scheduling.list', renderer='scheduling.mako')
def admin_vaccines_item(request):
  db = request.environ['db']
  rvalue = {
      'alerts': [Notification(message= 'OK', at=datetime.now())],
      'project': 'GET-A-VAX',
      'title': 'Agendamentos',
      'menu_entries': menu_entries(),
  }
  offset = int(request.params.get('offset', 0))
  limit = 25
  sql = """
    SELECT COUNT(*) cnt FROM
      vaccine_user_schedule_event_scheduled vses"""
  db.execute(sql)
  count = db.fetchone()['cnt']
  sql = """WITH data AS (
    SELECT * FROM
      vaccine_user_schedule_event_scheduled vses
      JOIN vaccine_user_schedule_event vse ON vses.id_vaccine_user_schedule_event=vses.id_vaccine_user_schedule_event
      JOIN user_ers u ON u.id_user_ers = vse.id_user_ers
      )
      SELECT * FROM data
      ORDER BY s_at_date DESC, s_at_time DESC, s_where ASC, ersid_user ASC
      LIMIT %s
      OFFSET %s"""
  db.execute(sql, (limit, offset, ))
  rvalue['records'] = db.fetchall()
  n = offset + limit
  rvalue['next_offset'] = None if n > count else n
  rvalue['prev_offset'] = None if offset < limit else offset - limit
  return rvalue

# vim: set et ts=2 sw=2  : 
