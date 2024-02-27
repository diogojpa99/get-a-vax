from pyramid.authentication import AuthTktCookieHelper
from pyramid.authorization import (
    ACLHelper,
    Authenticated,
    Everyone,
)

__all_groups__ = [
    'group:customer'
]

class MySecurityPolicy:
  def __init__(self, secret, /):
    self.authtkt = AuthTktCookieHelper(secret)
    self.acl = ACLHelper()
    return

  def identity(self, request):
    identity = self.authtkt.identify(request)
    return identity

  def authenticated_userid(self, request):
    identity = self.identity(request)
    if identity is not None:
      return identity['userid']
    return

  def remember(self, request, userid, **kw):
    return self.authtkt.remember(request, userid, **kw)

  def forget(self, request, **kw):
    return self.authtkt.forget(request, **kw)

  def permits(self, request, context, permission):
    principals = self.effective_principals(request)
    rvalue =  self.acl.permits(context, principals, permission)
    return rvalue

  def effective_principals(self, request):
    principals = [Everyone]
    identity = self.identity(request)
    if identity is not None:
      principals.append(Authenticated)
      principals.append('u:' + identity['userid'])
      principals.extend(__all_groups__)
    return principals





# vi: set ts=2 sw=2 : 
