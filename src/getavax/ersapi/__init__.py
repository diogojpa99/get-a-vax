
import datetime
import logging
import uuid

from pyramid.config import Configurator
from pyramid.view import view_config

from getavax import db

from sqlalchemy.exc import DBAPIError


__log__ = logging.getLogger(__name__)


@view_config(route_name='ersapi.confirm_shot', renderer='json')
def put_confirm_shot(request):
  
  rvalue = {}
  if not request.body:
    return None

  body = request.json_body
  id_vse = body['id_externo']
  vaccine_shot_date = datetime.date.fromisoformat(body['data'])
  ersid_clinic = body.get('centro')
  ersid_signed_by = body.get('clinico_responsavel')
  ersid_vaccine = body.get('id_vacina')
  vaccine_name = body.get('marca_vacina')
  vaccine_batch_number = body.get('lote_vacina')
  created_at = datetime.datetime.now()

  sql = """INSERT INTO vaccine_user_schedule_event_log
    (id_vaccine_user_schedule_event,vaccine_shot_date,ersid_clinic,ersid_signed_by,ersid_vaccine,vaccine_name,vaccine_batch_number,created_at)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)"""
  
  try:
    db = request.environ['db']
    db.execute(sql, (id_vse, vaccine_shot_date, ersid_clinic,
      ersid_signed_by,ersid_vaccine,vaccine_name,vaccine_batch_number,created_at))
    
    db.execute('SELECT id_user_ers FROM vaccine_user_schedule_event WHERE id_vaccine_user_schedule_event=%s', (id_vse,))
    id_user = db.fetchone()['id_user_ers']
    
    db.execute('SELECT name FROM clinic WHERE  ersid_clinic=%s', (ersid_clinic,))
    clinic_name = db.fetchone()['name']
    
    db.execute('''INSERT INTO vaccine_shcedule_event_bulletin 
              (id_vaccine_user_schedule_event, id_user, clinic_name, vaccine_shot_date, vaccine_name)
              VALUES (%s, %s, %s, %s, %s, %s, %s)''', (id_vse, id_user, clinic_name, vaccine_shot_date, vaccine_name,))
    
    db.connection.commit()
    
  except DBAPIError as e:
    db.connection.rollback()
    rvalue['error'] = str(e)
      
  return rvalue

@view_config(route_name='ersapi.client', renderer='json')
def ersapi_put_user(request):
  if len(request.body) == 0:
    return None

  body = request.json_body
  id_user_ers = uuid.uuid4()
  name = body['nome'] + ' ' + body['apelido']
  email = body['email']
  ersid_user=body['numero_utente']
  born_at = body['data_nascimento']

  db = request.environ['db']

  sql = """INSERT INTO user_ers (id_user_ers,name,email,ersid_user,born_at) VALUES (%s,%s,%s,%s,%s)"""
  db.execute(sql, (id_user_ers, name, email, ersid_user,born_at,))

  sql = """INSERT INTO user_base (id_user_base,id_user_ers) VALUES (%s,%s)"""
  db.execute(sql, (id_user_ers, id_user_ers,))

  sql = """INSERT INTO vaccine_user_configuration (id_vaccine_user_configuration, id_user_ers, id_vaccine, enabled)
  SELECT gen_random_uuid(),%s,v.id_vaccine,TRUE FROM vaccine v"""
  db.execute(sql, (id_user_ers,))

  rvalue = {}
  return rvalue


def main(global_config, **settings):

  s = global_config | settings

  db.setparams(name=s.get('db.name'), host=s.get('db.host'),
      user=s.get('db.user'), password=s.get('db.pass'))

  config = Configurator(settings=s)
  config.scan('.')
  config.add_tween('.db.tween_factory')

  config.add_route('ersapi.client', '/utentes')
  config.add_route('ersapi.confirm_shot', '/confirma')

  return config.make_wsgi_app()


# vi: set ts=2 sw=2 et : 


# To test using curl sending a POST request to http://127.0.0.1:6543/ersapi/utentes
# with the following JSON body:
# 
# {
#   "name": "John"",
#   "apelido": "Doe",
#   "email": "john.doe@example",
#   "numero_utente": "123456789",
#   "data_nascimento": "1970-01-01"
# }
#
# curl -X POST -d '{"nome": "John", "apelido": "Doe", "email": "john.doe@example", "numero_utente": "123456789", "data_nascimento": "1970-01-01"}' http://127.0.0.1:6543/ersapi/utentes

# 2nd test with Ann Doe
# curl -X POST -d '{"nome": "Ann", "apelido": "Doe", "email": "ann.doe@example", "numero_utente": "987654321", "data_nascimento": "1970-01-01"}' http://127.0.0.1:6543/ersapi/utentes
