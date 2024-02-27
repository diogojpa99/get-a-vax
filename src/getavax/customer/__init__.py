
from datetime import date, datetime
import uuid

import pyramid
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

from . import authentication, home
from .. import db
from ..security import MySecurityPolicy
from ..ui.alert import Alerts
from ..ui import TplHelper



def add_global(event):
  request = event['request']
  event['tpl'] = TplHelper(request)
  event['alerts'] = Alerts(request.session)
  return

def render_iso(o, request):
  return o.isoformat()

def render_uuid(o, request):
  return str(o)

def main(global_config, **settings):
  s = global_config | settings

  db.setparams(name=s.get('db.name'), host=s.get('db.host'),
      user=s.get('db.user'), password=s.get('db.pass'))

  config = Configurator(settings=s)
  config.add_subscriber('.add_global', 'pyramid.events.BeforeRender')
  config.include('pyramid_mako')

  authentication.includeme(config)
  home.includeme(config)
  config.scan('.')

  config.add_tween('getavax.db.tween_factory')
  config.add_static_view(name='static', path='getavax:public/')
  config.add_static_view(name='me', path='getavax.customer:me/')

  json_renderer = pyramid.renderers.JSON()
  json_renderer.add_adapter(datetime, render_iso)
  json_renderer.add_adapter(date, render_iso)
  json_renderer.add_adapter(uuid.UUID, render_uuid)
  config.add_renderer('json', json_renderer)

  security_policy = MySecurityPolicy('28a51853-7b9a-4d90-a614-6b8b6682a9da')
  config.set_security_policy(security_policy)
  session_factory = SignedCookieSessionFactory('0295cb63-8495-4913-87a5-caea06fde174')
  config.set_session_factory(session_factory)

  return config.make_wsgi_app()


# vi: set ts=2 sw=2 et : 
