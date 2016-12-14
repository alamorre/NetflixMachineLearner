from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_survey$', views.add_survey, name='add_survey'),
    url(r'^view_question_[0-9]$', views.view_question, name='view_question'),
    url(r'^view_database', views.view_database, name='view_database'),
    url(r'^recorder$', views.recorder, name='recorder'),
    url(r'^recorderWorker$', views.recorderWorker, name='recorderWorker'),
]
