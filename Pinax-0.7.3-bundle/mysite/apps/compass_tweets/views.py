from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext,loader
from compass_tweets.models import Context,Type, Role, Rule, ContextMember
from compass_tweets.forms import ContextForm, TypeForm, RoleForm
from compass_tweets.forms import ContextMemberFormSet
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django import forms
from django.forms.models import modelformset_factory

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def add_context(request,template_name = "compass_tweets/editcontext.html"):
	form = ContextForm(prefix="form")
	typeform=TypeForm(prefix="type")
	roleform=RoleForm(prefix="role")
	#ruleform=RuleForm(prefix="rule")
	if request.POST:

		if request.POST['action'] == 'context':
			form = ContextForm(request.user,request.POST, prefix="form")
			if form.is_valid():
				context = form.save(commit=False)
				context.save()
				form.save_m2m()
				request.session['context'] = context
				
				return HttpResponseRedirect(reverse('add_rules'))
				#return HttpResponseRedirect("compass_tweets/add_members.html",{"contextmemberformset": contextmemberformset, "context":context})
				#return HttpResponseRedirect(reverse('add_members', kwargs={'context':context})
				#return render(request,t.render(c),{"context": context,"contextmemberformset": contextmemberformset})
			else :
				form = ContextForm(prefix="form") 

		elif request.POST['action'] == 'type':
			typeform=TypeForm(request.POST, prefix = "type")
			if typeform.is_valid():
				typeform.save()

			typeform=TypeForm(prefix="type")

		elif request.POST['action'] == 'role':
			roleform=RoleForm(request.POST, prefix = "role")
			if roleform.is_valid():
				roleform.save()
			else:
				roleform=RoleForm(prefix="role")

	#	elif request.POST['action'] == 'rule':
	#		ruleform=RuleForm(request.POST, prefix = "rule")
	#		if ruleform.is_valid():
	#			ruleform.save()
	#		else:
	#			ruleform=RuleForm(prefix="rule")

	return render_to_response(template_name,{"form": form ,"typeform":typeform,"roleform":roleform,#"ruleform":ruleform,
	})

def make_rule_form(context):
	class RuleForm(forms.Form):
		message_type = forms.ModelChoiceField(context.types)
		sender_role = forms.ModelChoiceField(context.roles)
		receiver_role = forms.ModelChoiceField(context.roles)
	return RuleForm


def add_rules(request, template_name="compass_tweets/add_rules.html"):
	if not 'context' in request.session:
		raise Http404
	context = request.session['context']
	RuleForm = make_rule_form(context)
	RuleFormSet = modelformset_factory(Rule, form=RuleForm, extra =10)
	if request.POST:
		print "ok"
		ruleformset=RuleFormSet(request.POST, prefix='rules',queryset=Rule.objects.none())
		print "mistake"
		print ruleformset.data
		if ruleformset.is_valid():
			print "here"
			rules = ruleformset.save()
			for rule in rules:
				context.rules.add(rule)
			return HttpResponseRedirect(reverse('add_members'))
		else:
			return HttpResponse(ruleformset.errors)
			
	else:
		ruleformset=RuleFormSet(queryset=Rule.objects.none(), prefix='rules')
		return render_to_response(template_name,{"ruleformset":ruleformset,"contextname":context.name})


def add_members(request, template_name="compass_tweets/add_members.html"):
	if not 'context' in request.session:
		raise Http404
	context = request.session['context']
	if request.POST:
		contextmemberformset = ContextMemberFormSet(request.POST, prefix='members',queryset=ContextMember.objects.none())
		if contextmemberformset.is_valid():
			members = contextmemberformset.save(commit=False)
			for member in members:
				member.context = context
				member.save()
			del request.session['context']
			return HttpResponse("Context successfully populated!!")
		else:
			return HttpResponse(contextmemberformset.errors)
	else:
		contextmemberformset = ContextMemberFormSet(queryset=ContextMember.objects.none(), prefix='members')
		return render_to_response(template_name,{"contextmemberformset":contextmemberformset, "contextname":context.name})

def roles(request, template_name="compass_tweets/roles.html"):
	user = request.user
	if user ==None:
		raise Http404
	contextroles=ContextMember.objects.filter(member=user)
	contexts = [u.context.name for u in contextroles]
	roles = [u.role.name for u in contextroles]
	crs = zip(contexts,roles)
	return render_to_response(template_name,{"contextroles":crs})

def friends(request, template_name = "compass_tweets/friends.html"):
	pass
	
def newsfeed(request):
	return HttpResponse("Compass newsfeed ")
	
def contextdef(request):
	return HttpResponse("Compass context definitions")

def index(request):
	template_name = "compass_tweets/index.html"
	return render_to_response(template_name)
