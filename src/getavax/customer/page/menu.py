
from getavax.ui.menu import MenuEntry, MenuEntryHeading

def menu_entries():
  return [
    MenuEntry('Dashboard', 'fas fa-fw fa-tachometer-alt', '/admin', True),
    MenuEntryHeading('Configuração'),
    MenuEntry('Vacinas', 'fas fa-syringe', '/admin/vaccines'),
    MenuEntry('Locais', 'fas fa-clinic-medical', '/admin/clinics'),
    MenuEntryHeading('Processos'),
    MenuEntry('Agendamento', 'fas fa-calendar', '/admin/processes/scheduling'),
    MenuEntry('Utentes', 'fas fa-user-cog', '/admin/processes/users'),
  ]
