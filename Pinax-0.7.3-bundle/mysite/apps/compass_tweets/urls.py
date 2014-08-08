from django.conf.urls.defaults import *

from compass_tweets import views
urlpatterns = patterns('',
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^contextdef/$', views.contextdef, name='contextdef'),
    url(r'^add_contextinstance/', views.add_contextInstance, name='add_contextinstance'),
    url(r'^add_context/', views.add_context, name='add_context'),
    url(r'^all_contexts/', views.all_contexts, name='all_context'),
    url(r'^add_members/', views.add_members, name='add_members'),
    url(r'^add_rules/', views.add_rules, name='add_rules'),
    url(r'^roles/', views.roles, name='roles'),
    url(r'^friends/$',views.friends, name='friends'),
    url(r'^ContextDetail/(?P<group_name>[-\w]+)/$', views.contextdetails, name="context_detail"),
    url(r'^$', views.index, name='index'),
)

