#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.template.loader import get_template
from .models import Tutor, Student, Topic, Question, Result, Answer
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf

# Create your views here.
#_______________________________________________________________________________________________________________________

# def index(request):
#     return HttpResponse("Hello, everybody. You are at the exams index now.")
#_______________________________________________________________________________________________________________________

def show_list_of_topics(request):
    # Повертає СПИСОК всіх ТЕМ
    args = {}
    args.update(csrf(request))
    args['show_list_of_topics'] = Topic.objects.all()
    args['username'] = auth.get_user(request).username
    if not auth.get_user(request).is_staff:
    # Якщо авторизований студент, то показує його результат по кожній темі, яку він проходив
        args['marks_list_user'] = Result.objects.filter(student_id_id = auth.get_user(request).id)
    return render_to_response('exam/show_list_of_topics.html', args)
#_______________________________________________________________________________________________________________________

def show_questions_of_topic(request, topic_id = 1):
    # Повертає для вибраної теми СПИСОК ПИТАНЬ з варіантами відповідей --- ДЛЯ СТУДЕНТА
    # або СПИСОК студентів та їх РЕЗУЛЬТАТІВ --- ДЛЯ ТЬЮТОРА
    args = {}
    args.update(csrf(request))
    args['show_topic'] = Topic.objects.get(id = topic_id)
    args['show_questions'] = Question.objects.filter(topic_id_id = topic_id)
    args['show_answers'] = Answer.objects.all()

    answers_list = []
    def show_answers_list(show_questions, show_answers):
        # Повертає СПИСОК ВАРІАНТІВ ВІДПОВІДЕЙ вибраної теми
        for question in show_questions:
            answers_list.append(show_answers.filter(question_id_id = question.id))
        return answers_list

    args['answers_list'] = show_answers_list(args['show_questions'], args['show_answers'])

    marks_list = []
    def show_mark_for_student(students_list):
        # Повертає СПИСОК РЕЗУЛЬТАТІВ по вибраній темі
        for student in students_list:
            marks_list.extend(Result.objects.filter(student_id_id = student.id, topic_id_id = topic_id))
        return marks_list

    args['username'] = auth.get_user(request).username

    if auth.get_user(request).is_staff:
        # Якщо авторизований тьютор (з правами доступу до "admin site", is_staff = True)
        # повертає СПИСОК студентів та їх РЕЗУЛЬТАТИ по вибраній темі
        args['students_list'] = Student.objects.all()
        args['marks_list'] = show_mark_for_student(args['students_list'])
        if marks_list == []:
            args['error_msg'] = 'Thank You For Visiting, But Currently No One Took The Test Of This Topic.'
        return render_to_response('exam/show_all_results.html',args)
    else:
        # інакше (якщо авторизований студент)
        # повертає СПИСОК ПИТАНЬ з варіантами відповідей для вибраної теми
        return render_to_response('exam/show_questions_of_topic.html',args)
#_______________________________________________________________________________________________________________________

def exam_result(request, topic_id):
    # Обчислює та повертає РЕЗУЛЬТАТ ТЕСТУ для студента
    args = {}
    args.update(csrf(request))

    def count_mark(answers_list, marks_value = 0):
        for answer in answers_list:
            if request.POST('answer.id'):
                marks_value = marks_value + answer.is_correct
        return marks_value

    answers_list = []
    def show_answers_list(show_questions, show_answers):
        # Повертає СПИСОК ВАРІАНТІВ ВІДПОВІДЕЙ вибраної теми
        for question in show_questions:
            answers_list.append(show_answers.filter(question_id_id = question.id))
        return answers_list

    answers_list = show_answers_list(Question.objects.filter(topic_id_id = topic_id), Answer.objects.all())

    if not Result.objects.get(student_id_id = auth.get_user(request).id, topic_id_id = topic_id):
        final_result = Result.objects.create(student_id_id = auth.get_user(request).id, topic_id_id = topic_id)
    else:
        final_result = Result.objects.get(student_id_id = auth.get_user(request).id, topic_id_id = topic_id)

    final_result.mark = count_mark(answers_list)
    final_result.save()

    return render_to_response("exam/show_list_of_topics.html", args)
