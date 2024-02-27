from collections import namedtuple
from datetime import date, datetime
import uuid

import pyramid
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from .. import db
from ..ui.alert import Alerts
from ..ui import TplHelper


def add_global(event):
  request = event['request']
  event['tpl'] = TplHelper(request)
  event['alerts'] = Alerts(request.session)

def render_iso(o, request):
  return o.isoformat()

def main(global_config, **settings):
  s = global_config | settings

  db.setparams(name=s.get('db.name'), host=s.get('db.host'),
      user=s.get('db.user'), password=s.get('db.pass'))

  config = Configurator(settings=s)
  config.add_subscriber('.add_global', 'pyramid.events.BeforeRender')
  config.include('pyramid_mako')

  json_renderer = pyramid.renderers.JSON()
  json_renderer.add_adapter(datetime, render_iso)
  json_renderer.add_adapter(date, render_iso)
  config.add_renderer('json', json_renderer)

  from . import authentication, dashboard, user, scheduling, vaccine
  for m in [ authentication, dashboard, user, scheduling, vaccine ]:
    m.includeme(config)

  config.scan('.')

  config.add_tween('..db.tween_factory')
  config.add_static_view(name='/static', path='getavax:public')
  session_factory = SignedCookieSessionFactory('0295cb63-8495-4913-87a5-caea06fde174')
  config.set_session_factory(session_factory)

  return config.make_wsgi_app()






# vim: set et ts=2 sw=2  : 
