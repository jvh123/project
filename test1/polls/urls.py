from django.conf.urls import url
from polls import views
urlpatterns=[
    url(r'^$',views.IndexView.as_view(),name="index"),
    url(r'^(?P<pk>\d+)/$',views.ResultsView.as_view(),name='detall'),
    url(r'^(?P<pk>\d+)/results/$',views.ResultsView.as_view(),name="result"),
    url(r'^(?P<question_id>\d+)/vote/$',views.vote,name='vote'),
]
