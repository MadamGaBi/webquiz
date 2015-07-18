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
			# register_form.save()
			if request.POST.get('is_staff'):
				new_user = Tutor.objects.create_user(username = request.POST.get('username'),
													 first_name = request.POST.get('first_name'),
													 last_name = request.POST.get('last_name'),
													 email = request.POST.get('email'),
													 password = request.POST.get('password1'),
													 is_staff = True)

				new_user = auth.authenticate(username=register_form.cleaned_data['username'], password=register_form.cleaned_data['password'])
				auth.login(request, new_user)
				return HttpResponseRedirect ('/exam/')
				# args['register_success_msg'] = 'Registration Is Successful! Please Log In And Enjoy!'
				# return render_to_response('register/login.html',args)
			else:
				new_user = Student.objects.create_user(username = request.POST.get('username'),
													   first_name = request.POST.get('first_name'),
													   last_name = request.POST.get('last_name'),
													   email = request.POST.get('email'),
													   password = request.POST.get('password1'),
													   is_staff = False)
				new_user = auth.authenticate(username=register_form.cleaned_data['username'], password=register_form.cleaned_data['password'])
				auth.login(request, new_user)
				return HttpResponseRedirect ('/exam/')
		else:
			args['register_error_msg'] = 'Try again!'
			args['form'] = register_form
	args_template = RequestContext(request, args)
	return render_to_response('register/register.html', args_template)
#_______________________________________________________________________________________________________________________


