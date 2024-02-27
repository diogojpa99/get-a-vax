
class Alerts:
  store = {}

  def __init__(self, session, /):
    self.store = Alerts.store
    key = '_alertsid'
    if not key in session or session.new:
      import uuid
      self.ssid = str(uuid.uuid4())
      session[key] = self.ssid
    else:
      self.ssid = session[key]
    if not self.ssid in self.store:
      self.store[self.ssid] = []
    return

  def __len__(self, /):
    return self.__store().__len__()

  def __iter__(self, /):
    return self.__store().__iter__()

  def __store(self, /):
    return self.store[self.ssid]
