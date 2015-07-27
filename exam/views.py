#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response, redirect
from .models import Tutor, Student, Topic, Question, Result, Answer
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect

# Create your views here.
#_______________________________________________________________________________________________________________________

def show_list_of_topics(request):
    # Повертає СПИСОК всіх ТЕМ
    args = {}
    args.update(csrf(request))
    args['show_list_of_topics'] = Topic.objects.all()
    args['username'] = auth.get_user(request).username
    if auth.get_user(request).is_staff:
        args['add_topic'] = "Please, fill in the following fields to add a new topic."
    if not auth.get_user(request).is_staff:
    # Якщо авторизований студент, то показує його результат по кожній темі, яку він проходив
        args['marks_list_user'] = Result.objects.filter(student_id_id = auth.get_user(request).id)
    return render_to_response('exam/show_list_of_topics.html', args)
#_______________________________________________________________________________________________________________________

def addtopic(request):
    # Додає НОВУ ТЕМУ в базу даних
    if request.method == 'POST':
        new_topic = Topic.objects.create(topic_name = request.POST.get('topic_name'),
                                         topic_description = request.POST.get('topic_description'))
        new_topic.save()
        return HttpResponseRedirect('/exam/')
    else:
        return render_to_response('exam/show_list_of_topics.html')
#_______________________________________________________________________________________________________________________

def show_answers_list(show_questions, show_answers):
    # Повертає СПИСОК ВАРІАНТІВ ВІДПОВІДЕЙ вибраної теми
    answers_list = []
    for question in show_questions:
        answers_list.append(show_answers.filter(question_id_id = question.id))
    return answers_list
#_______________________________________________________________________________________________________________________

def show_mark_for_student(students_list, topic_id):
    # Повертає СПИСОК РЕЗУЛЬТАТІВ по вибраній темі
    marks_list = []
    for student in students_list:
        marks_list.extend(Result.objects.filter(student_id_id = student.id, topic_id_id = topic_id))
    return marks_list
#_______________________________________________________________________________________________________________________

def show_questions_of_topic(request, topic_id):
    # Повертає для вибраної теми СПИСОК ПИТАНЬ з варіантами відповідей --- ДЛЯ СТУДЕНТА
    # або СПИСОК студентів та їх РЕЗУЛЬТАТІВ --- ДЛЯ ТЬЮТОРА
    args = {}
    args.update(csrf(request))
    args['show_topic'] = Topic.objects.get(id = topic_id)
    args['show_questions'] = Question.objects.filter(topic_id_id = topic_id)
    args['show_answers'] = Answer.objects.all()
    args['answers_list'] = show_answers_list(args['show_questions'], args['show_answers'])
    args['username'] = auth.get_user(request).username

    if auth.get_user(request).is_staff:
        # Якщо авторизований тьютор (з правами доступу до "admin site", is_staff = True)
        # повертає СПИСОК студентів та їх РЕЗУЛЬТАТИ по вибраній темі
        args['students_list'] = Student.objects.all()
        args['marks_list'] = show_mark_for_student(args['students_list'], topic_id)
        if args['marks_list'] == []:
            args['error_msg'] = 'Thank You for visiting, but currently no one took the test of this topic.'
        args['add_question'] = "Please, fill in the following fields to add a new question to this topic."
        return render_to_response('exam/show_all_results.html', args)
    else:
        # інакше (якщо авторизований студент)
        # повертає СПИСОК ПИТАНЬ з варіантами відповідей для вибраної теми
        return render_to_response('exam/show_questions_of_topic.html', args)
#_______________________________________________________________________________________________________________________

def addquestion(request, topic_id):
    # Додає НОВЕ ПИТАННЯ з трьома варіантами відповідей для відповідної теми
    if request.method == 'POST':
        new_question = Question.objects.create(question_text = request.POST.get('question_text'),
                                               tutor_id_id = auth.get_user(request).id,
                                               topic_id_id = topic_id)
        new_question.save()
        new_answer_1 = Answer.objects.create(answer_text = request.POST.get('answer_text_1'),
                                           is_correct = request.POST.get('is_correct_1'),
                                           question_id_id = new_question.id)
        new_answer_1.save()
        new_answer_2 = Answer.objects.create(answer_text = request.POST.get('answer_text_2'),
                                           is_correct = request.POST.get('is_correct_2'),
                                           question_id_id = new_question.id)
        new_answer_2.save()
        new_answer_3 = Answer.objects.create(answer_text = request.POST.get('answer_text_3'),
                                           is_correct = request.POST.get('is_correct_3'),
                                           question_id_id = new_question.id)
        new_answer_3.save()
        return HttpResponseRedirect('/exam/')
    else:
        return render_to_response('exam/show_all_results.html')
#_______________________________________________________________________________________________________________________

def result(request, topic_id):
    # Обчислює та повертає РЕЗУЛЬТАТ ТЕСТУ для студента
    args = {}
    args.update(csrf(request))

    def count_mark(answers_list, marks_value = 0):
        # Повертає ОЦІНКУ за весь тест з обраної теми,
        # перевіряючи по списку всіх відповідей теми чи було прийняте відповідне значення id
        for answers in answers_list:
            for answer in answers:
                if str(answer.id) in request.POST.getlist('answer'):
                    marks_value += answer.is_correct
        return marks_value

    if not auth.get_user(request).is_staff:
        # Якщо авторизований студент
        answers_list = show_answers_list(Question.objects.filter(topic_id_id = topic_id), Answer.objects.all())
        if Result.objects.get(student_id_id = auth.get_user(request).id, topic_id_id = topic_id):
            final_result = Result.objects.get(student_id_id = auth.get_user(request).id, topic_id_id = topic_id)
        else:
            final_result = Result.objects.create(student_id_id = auth.get_user(request).id, topic_id_id = topic_id)
        # Викликає функцію обчислення загальної оцінки за весь тест
        final_result.mark = count_mark(answers_list)
        # та зберігає цю оцінку в базі даних
        final_result.save()
        args['show_topic'] = Topic.objects.get(id = topic_id)
        args['marks_value'] = final_result.mark

    return redirect("/exam/", args)
#_______________________________________________________________________________________________________________________
