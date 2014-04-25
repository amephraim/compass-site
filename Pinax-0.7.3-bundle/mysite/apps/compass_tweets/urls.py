from django.conf.urls.defaults import *

from compass_tweets import views

urlpatterns = patterns('',
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^contextdef/$', views.contextdef, name='contextdef'),
    #url(r'^$', views.index, name='index'),
)

