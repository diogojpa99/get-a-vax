
from getavax.ui.menu import MenuEntry, MenuEntryHeading

__entries__ = [
    MenuEntry('Dashboard', 'fas fa-fw fa-tachometer-alt', '/admin', True),
    MenuEntryHeading('Configuração'),
    MenuEntry('Vacinas', 'fas fa-syringe', '/admin/vaccines'),
    #MenuEntry('Locais', 'fas fa-clinic-medical', '/admin/clinics'),
    #MenuEntryHeading('Processos'),
    MenuEntry('Agendamento', 'fas fa-calendar', '/admin/scheduling'),
    #MenuEntry('Utentes', 'fas fa-user-cog', '/admin/processes/users'),
  ]

def menu_entries():
  return __entries__
