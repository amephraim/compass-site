from django.conf.urls.defaults import *

from compass_tweets import views
urlpatterns = patterns('',
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^contextdef/$', views.contextdef, name='contextdef'),
    
    url(r'^add_context/', views.add_context, name='add_context'),
    url(r'^add_members/', views.add_members, name='add_members'),
    url(r'^add_rules/', views.add_rules, name='add_rules'),
    url(r'^roles/', views.roles, name='roles'),
    url(r'^friends/$',views.friends, name='friends'),
    url(r'^$', views.index, name='index'),
)

