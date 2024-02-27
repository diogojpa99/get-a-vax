import json
import uuid

from dataclasses import dataclass
from datetime import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from getavax.ui.menu import MenuEntry, MenuEntryHeading

from ..page.menu import menu_entries
from ..page.notification import Notification

def includeme(config):
  config.add_route('admin.vaccine.list', '/vaccines')
  config.add_route('admin.vaccine.new',  '/vaccines/new')
  config.add_route('admin.vaccine.edit',  '/vaccines/{id}/edit')
  config.add_route('admin.vaccine.item',  '/vaccines/{id}')
  return


@view_config(route_name='admin.vaccine.item', renderer='page_item.mako')
def admin_vaccines_item(request):
  rvalue = {
      'alerts': [Notification(message= 'OK', at=datetime.now())],
      'project': 'GET-A-VAX',
      'title': 'Detalhe de vacina',
      'menu_entries': menu_entries(),
  }
  return rvalue

@view_config(route_name='admin.vaccine.list', renderer='page_list.mako')
def admin_vaccines_list(request):
  errors = []
  if request.method == 'POST':
    
    db = request.environ['db']
    id_vaccine = uuid.uuid4()
    db.execute("INSERT INTO vaccine (id_vaccine,name,ersid_vaccine) VALUES (%s,%s,%s)",
        (id_vaccine, request.POST.getone('vaccineName'), request.POST.getone('ersCode')))
    agemin_value = int(request.POST.get('ageMin', -1))
    agemax_value = int(request.POST.get('ageMax', -1))
    
    if agemax_value >= 0 and agemax_value < agemin_value:
      errors.append(('ageMax', 'tem de ser maior que o mínimo',))
    else:
      db.execute("""INSERT INTO vaccine_rules_age
       (id_vaccine, agemin_value,agemin_unit, agemax_value, agemax_unit)
      VALUES (%s, %s,%s,%s,%s) """, (id_vaccine, agemin_value, request.POST.getone('ageMinUnit'),
            agemax_value, request.POST.getone('ageMaxUnit'),))
    #
    db.execute("""INSERT INTO vaccine_rules_booster
        (id_vaccine, value, unit,value1, unit1,
         value2, unit2,value3, unit3,value4, unit4,value5, unit5,
         value6, unit6,value7, unit7,value8, unit8,value9, unit9)
        VALUES
        (%s,%s,%s,%s,%s,
         %s,%s,%s,%s,%s,%s,%s,%s,
         %s,%s,%s,%s,%s,%s,%s,%s)
""" ,(id_vaccine, request.POST.get('boosterVal', -1), request.POST.getone('boosterValUnit'),
           int(request.POST.get('boosterVal1', -1)), request.POST.getone('boosterVal1Unit'),
           int(request.POST.get('boosterVal2', -1)), request.POST.getone('boosterVal2Unit'),
           int(request.POST.get('boosterVal3', -1)), request.POST.getone('boosterVal3Unit'),
           int(request.POST.get('boosterVal4', -1)), request.POST.getone('boosterVal4Unit'),
           int(request.POST.get('boosterVal5', -1)), request.POST.getone('boosterVal5Unit'),
           int(request.POST.get('boosterVal6', -1)), request.POST.getone('boosterVal6Unit'),
           int(request.POST.get('boosterVal7', -1)), request.POST.getone('boosterVal7Unit'),
           int(request.POST.get('boosterVal8', -1)), request.POST.getone('boosterVal8Unit'),
           int(request.POST.get('boosterVal9', -1)), request.POST.getone('boosterVal9Unit'), ))

    if not errors:
      db.connection.commit()
      return HTTPFound(location=request.route_path('admin.vaccine.list'))
    
  rvalue = {
      'alerts': [Notification(message= 'OK', at=datetime.now())],
      'project': 'GET-A-VAX',
      'title': 'Vacinas',
      'menu_entries': menu_entries(),
  }
  
  if errors:
    db.connection.rollback()
    rvalue['alerts'] = [Notification(message= 'Erro', at=datetime.now())]
    rvalue['errors'] = errors
    
  return rvalue

@view_config(route_name='admin.vaccine.edit', renderer='page_edit.mako')
def admin_vaccines_edit(request):
  errors = []
  if request.method == "POST":
    db = request.environ['db']
    id_vaccine = request.matchdict['id']
    db.execute("UPDATE vaccine SET name=%s, ersid_vaccine=%s WHERE id_vaccine=%s",
        (request.POST.getone('vaccineName'), request.POST.getone('ersCode'), id_vaccine))
    agemin_value = int(request.POST.get('ageMin', -1))
    agemax_value = int(request.POST.get('ageMax', -1))
    if agemax_value >= 0 and agemax_value < agemin_value:
      errors.append(('ageMax', 'tem de ser maior que o mínimo',))
    else:
      db.execute("""UPDATE vaccine_rules_age
      SET agemin_value=%s,agemin_unit=%s, agemax_value=%s, agemax_unit=%s
      WHERE id_vaccine=%s""", (agemin_value, request.POST.getone('ageMinUnit'),
            agemax_value, request.POST.getone('ageMaxUnit'), id_vaccine,))
    #
    db.execute("""UPDATE vaccine_rules_booster
    SET value=%s, unit=%s,value1=%s, unit1=%s,
        value2=%s, unit2=%s,value3=%s, unit3=%s,value4=%s, unit4=%s,value5=%s, unit5=%s,
        value6=%s, unit6=%s,value7=%s, unit7=%s,value8=%s, unit8=%s,value9=%s, unit9=%s
    WHERE id_vaccine=%s""" ,(request.POST.get('boosterVal', -1), request.POST.getone('boosterValUnit'),
           int(request.POST.get('boosterVal1', -1)), request.POST.getone('boosterVal1Unit'),
           int(request.POST.get('boosterVal2', -1)), request.POST.getone('boosterVal2Unit'),
           int(request.POST.get('boosterVal3', -1)), request.POST.getone('boosterVal3Unit'),
           int(request.POST.get('boosterVal4', -1)), request.POST.getone('boosterVal4Unit'),
           int(request.POST.get('boosterVal5', -1)), request.POST.getone('boosterVal5Unit'),
           int(request.POST.get('boosterVal6', -1)), request.POST.getone('boosterVal6Unit'),
           int(request.POST.get('boosterVal7', -1)), request.POST.getone('boosterVal7Unit'),
           int(request.POST.get('boosterVal8', -1)), request.POST.getone('boosterVal8Unit'),
           int(request.POST.get('boosterVal9', -1)), request.POST.getone('boosterVal9Unit'),
           id_vaccine, ))
    
    if not errors:
      db.connection.commit()
      return HTTPFound(location=request.route_path('admin.vaccine.list'))
    
  rvalue = {
      'alerts': [Notification(message= 'OK', at=datetime.now())],
      'project': 'GET-A-VAX',
      'title': 'Vacinas',
      'menu_entries': menu_entries(),
  }
  
  if errors:
    db.connection.rollback()
    rvalue['alerts'] = [Notification(message= 'Erro', at=datetime.now())]
    rvalue['errors'] = errors

  return rvalue

@view_config(route_name='admin.vaccine.new', renderer='page_new.mako')
def admin_vaccines_new(request):
  rvalue = {
      'alerts': [],
      'project': 'GET-A-VAX',
      'menu_entries': menu_entries(),
      'title': 'Nova vacina',
  }
  return rvalue

# vim: set et ts=2 sw=2  : 
