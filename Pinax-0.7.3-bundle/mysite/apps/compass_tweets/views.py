from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from compass_tweets.models import Context,Type, Role, Rule
from compass_tweets.forms import ContextForm, TypeForm, RoleForm,RuleForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def add_context(request,template_name = "compass_tweets/editcontext.html"):
	form = ContextForm(prefix="context")
	typeform=TypeForm(prefix="type")
	roleform=RoleForm(prefix="role")
	ruleform=RuleForm(prefix="rule")
	if request.POST:
		
		if request.POST['action'] == 'context':
			form = ContextForm(request.user,request.POST, prefix="form")
			if form.is_valid():
				context = form.save(commit=False)
				context.save()
				form.save_m2m()
			else :
				form = ContextForm(prefix="context")
				
		elif request.POST['action'] == 'type':
			typeform=TypeForm(request.POST, prefix = "type")
			if typeform.is_valid():
				typeform.save()
			
			typeform=TypeForm(prefix="type")
				
		elif request.POST['action'] == 'role':
			roleform=RoleFormSet(request.POST, prefix = "role")
			if roleform.is_valid():
				roleform.save()
			else:
				roleform=RoleForm(prefix="role")
		
		elif request.POST['action'] == 'rule':
			ruleform=RoleForm(request.POST, prefix = "rule")
			if ruleform.is_valid():
				ruleform.save()
				print "saved rulefomr"
			else:
				ruleform=RuleForm(prefix="rule")
				print "didn't save"
		
	return render_to_response(template_name,{"form": form ,"typeform":typeform,"roleform":roleform,"ruleform":ruleform,})

def friends(request, template_name = "compass_tweets/friends.html"):
	pass
	
def newsfeed(request):
	return HttpResponse("Compass newsfeed ")
	
def contextdef(request):
	return HttpResponse("Compass context definitions")

def index(request):
	template_name = "compass_tweets/index.html"
	return render_to_response(template_name)
