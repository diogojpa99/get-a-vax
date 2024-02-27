
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import (
    forget,
    remember,
)
from pyramid.view import view_config

def includeme(config):
  config.add_route('customer.login', '/login')
  config.add_route('customer.logout', '/logout')
  return


@view_config(route_name='customer.login', renderer='login.mako')
def customer_login(request):
  session = request.session
  if request.method == 'POST':
    step = session['lstate'] if 'lstate' in session else 'step1'
    if step == 'step1':
      db = request.environ['db']
      ersid = request.POST['ersid']
      born_at = request.POST['born_at']
      db.execute('''SELECT *
      FROM user_base ub
      INNER JOIN user_ers ue ON ub.id_user_ers = ue.id_user_ers
      WHERE ue.ersid_user=%s AND ue.born_at=%s''', (ersid,born_at))
      r = db.fetchone()
      if r:
        step = 'step2'
        session['uid'] = str(r['id_user_ers'])
        session['lstate'] = step
        session.changed()
    elif step == 'step2':
      session.pop('lstate', None)
      login = session.pop('uid', None)
      #session.changed()
      headers = remember(request, login)
      return HTTPSeeOther(location=request.route_url('customer.home'),
          headers = headers)
    else:
      raise Exception(f'something wrong with login step={step}')
  else:
    step = 'step1'
    if not session.new:
      session.invalidate()
  return {'step': step }


@view_config(route_name='customer.logout')
def customer_logout(request):
  headers = forget(request)
  request.session.invalidate()
  return HTTPSeeOther(
      location=request.route_url('customer.login'),
      headers=headers,
  )



# vi: set sw=2 ts=2 et : 
