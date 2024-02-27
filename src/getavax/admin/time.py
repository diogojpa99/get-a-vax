

from dataclasses import dataclass
from datetime import timedelta


__time_units_in_days__ = {
    'd': 1,
    'm': 30,
    'y': 365,
}

def days(value, unit):
  return value * __time_units_in_days__[unit]

@dataclass
class Interval:
  value:int
  unit:str

  def days(self,):
    return days(self.value, self.unit)

  def timedelta(self,):
    return timedelta(days=self.days())

  def isvalid(self):
    return self.unit in __time_units_in_days__

# vim: set et ts=2 sw=2  : 
