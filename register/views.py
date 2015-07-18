#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from .forms import UserCreateForm
from django.template import RequestContext
from django.db import IntegrityError
from exam.models import Tutor, Student, Topic, Question, Result, Answer

# Create your views here.
#_______________________________________________________________________________________________________________________

def login(request):
	"""
	    Авторизація користувача
	"""
	args = {}
	args.update(csrf(request))
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			# якщо користувач з відповідними username та password знайдений
			auth.login(request, user)
			return redirect('/exam/')
		else:
			# якщо користувач з відповідними username та password НЕ знайдений
			args['login_error'] = "User is not found"
			return render_to_response('register/login.html',args)
	else:
		return render_to_response('register/login.html',args)
#_______________________________________________________________________________________________________________________

def logout(request):
	"""
	    Деавторизація користувача
	"""
	auth.logout(request)
	return redirect('/exam/')
#_______________________________________________________________________________________________________________________

def register(request):
	"""
	    Реєстрація нового користувача
	"""
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreateForm()
	if request.method == 'POST':
		register_form = UserCreateForm(request.POST)
		if register_form.is_valid():
			# перевірка правильності всіх полів форми
			if request.POST.get('is_staff'):
				# якщо отримано запит на права доступу до "admin site" (поле is_staff відмічене)
				# створює користувача в таблиці Tutor і зберігає в БД
				new_user = Tutor.objects.create_user(username = request.POST.get('username'),
													 first_name = request.POST.get('first_name'),
													 last_name = request.POST.get('last_name'),
													 email = request.POST.get('email'),
													 password = request.POST.get('password1')
													 )
				new_user.is_staff = True
				new_user.save()
				new_user = auth.authenticate(username = request.POST.get('username'), password = request.POST.get('password1'))
				auth.login(request, new_user)
				# авторизує користувача та повертає головну сторінку
				return HttpResponseRedirect ('/exam/')
			else:
				# якщо НЕ отримано запит на права доступу до "admin site" (поле is_staff НЕ відмічене)
				# створює користувача в таблиці Student і зберігає в БД
				new_user = Student.objects.create_user(username = request.POST.get('username'),
													 first_name = request.POST.get('first_name'),
													 last_name = request.POST.get('last_name'),
													 email = request.POST.get('email'),
													 password = request.POST.get('password1')
													 )
				new_user.is_staff = False
				new_user.save()
				new_user = auth.authenticate(username = request.POST.get('username'), password = request.POST.get('password1'))
				auth.login(request, new_user)
				# авторизує користувача та повертає головну сторінку
				return HttpResponseRedirect ('/exam/')
		else:
			# якщо поля форми заповнені НЕ правильно,
			# повертає повідомлення про помилку та форму реєстрації
			args['register_error_msg'] = 'Try again!'
			args['form'] = register_form
	args_template = RequestContext(request, args)
	return render_to_response('register/register.html', args_template)
#_______________________________________________________________________________________________________________________


