from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/', 'register.views.login'),
    url(r'^logout/', 'register.views.logout'),
    url(r'^register/', 'register.views.register'),
)