
import datetime

__all__ = [ 'menu' ]



class TplHelper:
    def __init__(self, request, /):
        self.request = request
        self.id = 0
        self.now = datetime.datetime.now()
        return
    def static_url(self, target, /):
        return self.request.static_path('getavax:public' + target)
    def url(self, target, /):
        return self.request.static_path('getavax:public/sb-admin-2' + target)

    def genid(self, prefix=''):
        self.id += 1
        return 'genid_' + prefix + str(self.id)
