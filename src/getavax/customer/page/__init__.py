
from pyramid.authorization import Allow


from getavax.ui.menu import MenuEntry, MenuEntryHeading

__entries__ = [
    MenuEntry('Faqs.', 'fas fa-fw fa-tachometer-alt', '/c/static/faqs.html', True),
    #MenuEntryHeading('Configuração'),
    #MenuEntry('Vacinas', 'fas fa-syringe', '/admin/vaccines'),
    #MenuEntry('Locais', 'fas fa-clinic-medical', '/admin/clinics'),
    #MenuEntryHeading('Processos'),
    #MenuEntry('Agendamento', 'fas fa-calendar', '/admin/scheduling'),
    #MenuEntry('Utentes', 'fas fa-user-cog', '/admin/processes/users'),
  ]
class Base:
  __acl__ =  [
      (Allow, 'group:customer', 'view'),
  ]

  def __init__(self, request, title):
    self.project = 'Portal Utentes'
    self.title = title
    return

  def menu_entries(self):
      return __entries__

