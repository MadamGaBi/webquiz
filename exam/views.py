#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.template.loader import get_template
# from django.views import generic
from .models import Tutor, Student, Topic, Question, Result, Answer
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf

# Create your views here.
#_______________________________________________________________________________________________________________________

def index(request):
    return HttpResponse("Hello, everybody. You are at the exams index now.")

def topics(request, topic_id):
    t = get_template('exam/topic.html')
    html = t.render(Context({'name': topic_id}))
    return HttpResponse(html)

def questions(request, question_id, topic_id):
    t = get_template('exam/question.html')
    html = t.render(Context({'name_1': question_id, 'name_2': topic_id}))
    return HttpResponse(html)

def results(request, topic_id, student_id):
    t = get_template('exam/result.html')
    html = t.render(Context({'name_1': Topic.objects.get(id = topic_id), 'name_2': Result.objects.get(student_id_id = student_id, topic_id_id = topic_id)}))
    return HttpResponse(html)
#_______________________________________________________________________________________________________________________

def show_list_of_topics(request):
    #Повертає СПИСОК всіх ТЕМ
    return render_to_response("exam/show_list_of_topics.html", {'show_list_of_topics': Topic.objects.all(),
                                                                'username': auth.get_user(request).username
                                                                })
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

# class ResultView(generic.DetailView):
#     model = Result
#     template_name = "exam/result.html"
#_______________________________________________________________________________________________________________________
#
# def exam_ticket(request, topic_id = 1):
#     p = get_object_or_404(Topic, pk = topic_id)
#     try:
#         selected_answer = p.answer_text_set.get(pk = request.POST['answer_text'])
#     except(KeyError, Answer.DoesNotExist):
#         return render(request, "exam/show_questions_of_topic.html", {
#          'questions': p,
#          'error_message': "",
#         })
#     else:
#         if selected_answer.is_correct != 0:
#             result.mark += selected_answer.is_correct
#             result.mark.save()






