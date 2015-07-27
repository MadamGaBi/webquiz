from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /exam/
    url(r'^$', views.show_list_of_topics),
    url(r'^addtopic/$', views.addtopic),
    # ex: /exam/5/
    url(r'^(?P<topic_id>[0-9]+)/$', views.show_questions_of_topic),
    url(r'^(?P<topic_id>[0-9]+)/result/$', views.result),
    url(r'^(?P<topic_id>[0-9]+)/addquestion/$', views.addquestion),
]

