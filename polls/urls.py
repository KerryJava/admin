from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
   # ex: /polls/5/
   # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    url(r'^snippet_list$', views.snippet_list, name='vote'),
]
