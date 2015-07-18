from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    # ex: /exam/
    #url(r'^$', views.index, name='index'),
    #ex: /exam/5/
    #url(r'^(?P<topic_id>[0-9]+)/$', 'exam.views.topics'),
    # ex: /exam/5/5/
    #url(r'^(?P<topic_id>[0-9]+)/(?P<question_id>[0-9]+)/$', 'exam.views.questions'),
    # ex: /exam/5/5/result/
    #url(r'^(?P<topic_id>[0-9]+)/(?P<student_id>[0-9]+)/results/$', 'exam.views.results'),
    # ex: /exam/
    url(r'^$', views.show_list_of_topics),
    # ex: /exam/topics/5/
    url(r'^(?P<topic_id>[0-9]+)/$', views.show_questions_of_topic),
    # ex: /exam/5/5/results/
    url(r'^(?P<topic_id>[0-9]+)/(?P<student_id>[0-9]+)/results/$', 'exam.views.results'),
]

