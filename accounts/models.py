import uuid
from django.db import models
from django.contrib import auth

#auth.signals.user_logged_in.disconnect(auth.models.update_last_login)
# 关于manage.py migrate无效的问题
# https://blog.csdn.net/qq_25730711/article/details/60327344
class User(models.Model):
	email = models.EmailField(primary_key=True)

	REQUIRED_FIELDS = []
	USERNAME_FIELD = 'email'
	is_anonymous = False
	is_authenticated = True

class Token(models.Model):

	email = models.EmailField()
	uid = models.CharField(default=uuid.uuid4, max_length=40)
