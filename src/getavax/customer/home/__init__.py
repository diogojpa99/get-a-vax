
import datetime
import itertools
import json
import urllib.request
import uuid

from ... import sendmail

from pyramid.httpexceptions import HTTPSeeOther
from pyramid.view import view_config

from ..page import Base

from getavax.admin.dashboard.availability import put as dashboard_push_availability
__ers_baseurl__ = 'http://localhost:5000'

class CustomerHome(Base):
  def __init__(self, request):
    super().__init__(request, title="Entrada")
    return

class CustomerSchedule(Base):
  def __init__(self, request):
    super().__init__(request, title="Agendar vacina")
    self.id_vse = request.matchdict.get('id_vse')
    return

def includeme(config):
  global __ers_baseurl__
  __ers_baseurl__ = config.get_settings().get('ersapi.baseurl', 'http://localhost:5000')
  config.add_route('customer.home', '/home', factory=CustomerHome)
  config.add_route('customer.schedule', '/schedule/{id_vse}', factory=CustomerSchedule)
  return




@view_config(route_name='customer.home', renderer='home.mako',
    permission='view')
def customer_home(request):
  return {'today': datetime.date.today() }

@view_config(route_name='customer.schedule', renderer='schedule.mako', permission='view')
def customer_schedule(request):
  
  step = int(request.params.get('step', 0))
  rvalue = {'step': step, 'id_vse': request.context.id_vse, 'error': {} }
  today = datetime.date.today()

  if step == 0 or (step == 2 and 'back' in request.POST):
    rvalue['clinic'] = request.params.get('clinic', None)
    rvalue['at'] = request.params.get('at', datetime.date.today() + datetime.timedelta(3))
    rvalue['step'] = 0
    rvalue['scheduling_date_min'] = str(today)
    
  elif step == 1:
    _from = datetime.date.fromisoformat(request.POST['at'])
    # Não permite agendar para hoje ou para o passado
    if  _from <= today:
      rvalue['clinic'] = request.params.get('clinic', None)
      rvalue['at'] = request.params.get('at', datetime.date.today() + datetime.timedelta(3))
      rvalue['step'] = 0
      rvalue['scheduling_date_min'] = str(today)
      rvalue['error']['at'] = "Não pode ser no passado ou hoje"
      request.response.status = 400
      return rvalue
    clinic = request.POST['clinic']
    data = do_fetch_availability(clinic, _from)
    rvalue['availability'] = group_availability(data['disponibilidade'])
    rvalue['step'] = 1
    rvalue['clinic'] = request.POST['clinic']
    rvalue['at'] = request.POST['at']
    dashboard_push_availability((rvalue['clinic'], data['disponibilidade']))
    
  elif step == 2:
    rvalue['at'] = request.params.get('at', datetime.date.today() + datetime.timedelta(3))
    db = request.environ['db']
    clinic = request.POST['clinic']
    timeslot = request.POST['timeslot']
    reserva_id = str(uuid.uuid4())
    reqbody_data = {
      'reserva_id': reserva_id,
      'centro': clinic,
      'reserva_horaria': timeslot,
      'utente': request.authenticated_userid,
    }    
    reqbody = json.dumps(reqbody_data).encode('UTF-8')
    url = urllib.parse.urljoin(__ers_baseurl__, '/reserva')
    r = urllib.request.Request(url, reqbody)
    r.add_header('Content-Type', 'application/json; charset=utf-8')
    r.add_header('Content-Length', len(reqbody))
    with urllib.request.urlopen(r) as f:
      rsp = json.load(f)
      
    if 'error' in rsp:
      clinic = request.POST['clinic']
      rvalue['clinic'] = clinic
      rvalue['at'] = request.POST['at']
      rvalue['error'] = f"Aconteceu um erro (código: {rsp.get('code')})"
      if rsp.get('code') == '12358':
        rvalue['error'] = "O utente não é elegível para o agendamento. Por favor contacte os serviços por outros meios."
      rvalue['step'] = 1
      _from = datetime.date.fromisoformat(request.POST['at'])
      data = do_fetch_availability(clinic, _from)
      rvalue['availability'] = group_availability(data['disponibilidade'])
      return rvalue
    
    id_vaccine_user_schedule_event = request.POST['id_vse']
    db.execute(
        'SELECT vse.* FROM vaccine_user_schedule_event vse WHERE vse.id_vaccine_user_schedule_event=%s',
        (id_vaccine_user_schedule_event,))
    
    if not db.rowcount:     # Check if the last query returned a row
      request.response.status = 400
      return {'error': 'Agendamento não encontrado'}
    
    at = datetime.datetime.fromisoformat(request.POST['timeslot']) # Acho que isto não está totalmente correto...
    s_at_date = datetime.datetime.strptime(rvalue['at'], "%Y-%m-%d").date() # This is the correct way to do it
    s_at_time = at.time()
    
    db.execute('SELECT c.name FROM clinic c WHERE c.id_clinic=%s', (clinic,))
    s_where = db.fetchone()['name']
    
    db.execute('''SELECT v.* FROM
        vaccine v
        INNER JOIN vaccine_user_schedule_event vse ON vse.id_vaccine=v.id_vaccine
        WHERE vse.id_vaccine_user_schedule_event=%s''', (id_vaccine_user_schedule_event,))
    s_what = db.fetchone()['name']
    
    # Do not insert if already exists
    # Check if the id_vaccine_user_schedule_event is already in the table
    # To do that, we use a subquery to get the id_vaccine_user_schedule_event
    db.execute('''SELECT id_vaccine_user_schedule_event FROM
        vaccine_user_schedule_event_scheduled
        WHERE id_clinic=%s AND s_at_date=%s AND s_at_time=%s AND s_where=%s AND s_what=%s''',
        (clinic, s_at_date, s_at_time, s_where, s_what))
    
    if db.rowcount == 0:
      db.execute("""INSERT INTO vaccine_user_schedule_event_scheduled 
          (id_vaccine_user_schedule_event,id_clinic, s_at_date, s_at_time, s_where,s_what)
          VALUES (%s,%s,%s,%s,%s,%s)""",
          (id_vaccine_user_schedule_event, clinic, s_at_date, s_at_time, s_where, s_what))
      
      db.execute("""SELECT name FROM user_ers 
                          WHERE id_user_ers = %s""", 
                          (request.authenticated_userid,))
      
      if db.rowcount == 0:
        raise Exception("User not found")
      elif db.rowcount > 0:
        print("User found"); c_name = db.fetchone()[0] 
      elif db.rowcount > 1:
        raise Exception("More than one user found")
      
      db.execute("""SELECT email FROM user_ers 
                          WHERE id_user_ers = %s""", 
                          (request.authenticated_userid,))
      
      c_email = db.fetchone()[0]
      
      ### Send confirmation email
      sendmail.send_confirm_mail(c_name, 
                                c_email, 
                                s_what, 
                                str(s_at_date), 
                                str(s_at_time), 
                                s_where)
          
  
    db.connection.commit()
    return HTTPSeeOther(request.route_path('customer.home'))
  else:
    raise Exception(step)
  return rvalue

      
def do_fetch_availability(clinic, _from):
  to = _from + datetime.timedelta(1)
  params = {'desde': _from, 'a': to, 'centro': clinic }
  url = urllib.parse.urljoin(__ers_baseurl__, '/disponibilidade?' + urllib.parse.urlencode(params))
  with urllib.request.urlopen(url) as f:
    rvalue = json.load(f)
  return rvalue

def group_availability(availability):
  rvalue = {}
  for isots, count in availability:
    isodt = datetime.datetime.fromisoformat(isots)
    h = isodt.hour
    m = isodt.minute
    if not h in rvalue:
      rvalue[h] = {}
    mdict = rvalue[h]
    hm = isodt.strftime('%H:%M')
    mdict[m] = (isodt, hm, count > 0 )
  return rvalue

# vi: set ts=2 sw=2 et : 
