from dataclasses import dataclass

import datetime

@dataclass
class Notification(object):
    message: str
    at: datetime.datetime
    is_new: bool = True



