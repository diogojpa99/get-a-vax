
from datetime import date
import unittest


from . import *
from getavax.admin.time import Interval

no_interval = Interval(None,None)

class TestRulesSample(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(1, 1)
        return
    
    def test_next(self):
        born_at = date(2021, 10, 4)
        at = date(2022, 5, 6)
        last = None
        interval6m = Interval(6,'m')
        rules = Rules(
                agemin = interval6m,
                agemax = no_interval,
                period = interval6m,
                fixed_intervals = [])
        self.assertEqual(rules.next(born_at, at, last), date(2022, 5, 6))
        return
    
    def test_next2(self):
        born_at = date(2019, 3, 1)
        at = date(2020, 2, 28)
        last = None
        interval1y = Interval(1,'y')
        rules = Rules(
                agemin = interval1y,
                agemax = no_interval,
                period = interval1y,
                fixed_intervals = [])
        self.assertEqual(rules.next(born_at, at, last), None)
        return
    
    def test_next3(self):
        born_at = date(2019, 3, 1)
        at = date(2020, 2, 29)
        last = None
        interval1y = Interval(1,'y')
        rules = Rules(
                agemin = interval1y,
                agemax = no_interval,
                period = interval1y,
                fixed_intervals = [])
        self.assertEqual(rules.next(born_at, at, last), date(2020, 2, 29))
        return





if __name__ == '__main__':
    unittest.main()
