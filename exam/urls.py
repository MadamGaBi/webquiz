from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
    # ex: /exam/
    url(r'^$', views.show_list_of_topics),
    url(r'^addtopic/$', views.addtopic),
    # url(r'^addquestion/$', views.addquestion),
    # ex: /exam/5/
    url(r'^(?P<topic_id>[0-9]+)/$', views.show_questions_of_topic),
    url(r'^(?P<topic_id>[0-9]+)/result/$', views.result),
]

