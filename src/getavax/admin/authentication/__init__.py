
import hashlib

from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import (
    forget,
    remember,
)
from pyramid.view import view_config


__salt__ = 'some really really long random text.'.encode('utf-8')
__iterations__ = 125093

def includeme(config):
  config.add_route('admin.login', '/login')
  config.add_route('admin.logout', '/logout')
  config.add_route('adminsrv.hash', '/srv/hash')
  return


@view_config(route_name='admin.login', renderer='login.mako')
def admin_login(request):
  session = request.session
  if request.method == 'POST':
    step = session['lstate'] if 'lstate' in session else 'step1'
    if step == 'step1':
      db = request.environ['db']
      email = request.POST['email']
      db.execute('''SELECT *
      FROM user_base ub
      INNER JOIN user_admin ua ON ub.id_user_admin = ua.id_user_admin
      WHERE ua.email=%s''', (email, ))
      r = db.fetchone()
      if r:
        secret = request.POST['secret']
        hashed_secret = hashlib.pbkdf2_hmac('sha256', secret.encode('utf-8'), __salt__, __iterations__).hex()
        if r['secret'] == hashed_secret:
          step = 'step2'
          session['uid'] = str(r['id_user_ers'])
          session['lstate'] = step
          session['nav_display_name'] = r['email']
          session.changed()
        else:
          # TODO: feedback
          pass
    elif step == 'step2':
      session.pop('lstate', None)
      login = session.pop('uid', None)
      #session.changed()
      headers = remember(request, login)
      return HTTPSeeOther(location=request.route_url('admin.dashboard'),
          headers = headers)
    else:
      raise Exception(f'something wrong with login step={step}')
  else:
    step = 'step1'
    if not session.new:
      session.invalidate()
  return {'step': step }


@view_config(route_name='admin.logout')
def admin_logout(request):
  headers = forget(request)
  request.session.invalidate()
  return HTTPSeeOther(
      location=request.route_url('admin.login'),
      headers=headers,
  )


@view_config(route_name='adminsrv.hash', renderer='json')
def admin_do_hash(request):
  rvalue = {}
  import json
  secret = json.loads(request.body)['value']
  rvalue['value'] =  hashlib.pbkdf2_hmac('sha256', secret.encode('utf-8'), __salt__, __iterations__).hex()
  return rvalue



# vi: set sw=2 ts=2 et : 
