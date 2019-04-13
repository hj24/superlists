from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import auth, messages
from accounts.models import Token
from django.urls import reverse
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout
#from django.contrib.auth import authenticate
import sys

# Create your views here.
def send_login_email(request):
	email = request.POST['email']
	token = Token.objects.create(email=email)
	# django中构建完整url的一种方式，所得url包括域名和协议(http/https)
	url = request.build_absolute_uri(
		reverse('login') + '?token=' + str(token.uid)
	)
	message_body = f'Use this link to log in:\n\n{url}'
	send_mail(
		'Your login link for Superlists',
		message_body,
		'noreply@superlists',
		[email]
	)
	messages.success(
		request,
		"Check your email, we've sent you a link you can use to log in."
	)
	return redirect('/')

def login(request):
	user = auth.authenticate(uid=request.GET.get('token'))
	print('*************',user)
	if user is not None:
		auth.login(request, user)
	return redirect('/')

def logout(request):
	auth.logout(request)
	return redirect('/')
