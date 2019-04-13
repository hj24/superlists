import sys
from accounts.models import User, Token

class PasswordlessAuthenticationBackend(object):
	# django 2.0以上的版本，定制authenticate要传入request
	def authenticate(self, request, uid):
		print('uid', uid, file=sys.stderr)
		try:
			token = Token.objects.get(uid=uid)
			return User.objects.get(email=token.email)
		except User.DoesNotExist:
			print('new user', file=sys.stderr)
			return User.objects.create(email=token.email)
		except Token.DoesNotExist:
			return None 

	def get_user(self, email):
		try:
			return User.objects.get(email=email)
		except User.DoesNotExist:
			return None