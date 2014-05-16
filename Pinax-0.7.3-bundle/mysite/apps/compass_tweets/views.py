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
from django.forms.models import formset_factory
from django.contrib.auth.models import User

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def add_context(request,template_name = "compass_tweets/editcontext.html"):
	form = ContextForm(prefix="form")
	typeform=TypeForm(prefix="type")
	roleform=RoleForm(prefix="role")
	if request.POST:
		if request.POST['action'] == 'context':
			form = ContextForm(request.user,request.POST, prefix="form")
			if form.is_valid():
				context = form.save(commit=False)
				context.save()
				form.save_m2m()
				request.session['context'] = context
				
				return HttpResponseRedirect(reverse('add_rules'))
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
	RuleFormSet = formset_factory(form=RuleForm, extra =10)
	if request.POST:
		ruleformset=RuleFormSet(request.POST, prefix='rules')
		print ruleformset.data
		if ruleformset.is_valid():
			for rf in ruleformset.forms:
				if not rf.cleaned_data.get('message_type') == None: #terrible hack, please correct
					message = rf.cleaned_data.get('message_type')
					sender = rf.cleaned_data.get('sender_role')
					receiver = rf.cleaned_data.get('receiver_role')
					rule, created = Rule.objects.get_or_create(message_type=message,sender_role=sender,receiver_role=receiver)
					if not created:
						rule.save()
					context.rules.add(rule)
			return HttpResponseRedirect(reverse('add_members'))
		else:
			return HttpResponse(ruleformset.errors)
			
	else:
		ruleformset=RuleFormSet(prefix='rules')
		return render_to_response(template_name,{"ruleformset":ruleformset,"contextname":context.name})

def make_member_form(context):
	class MemberForm(forms.Form):
		member = forms.ModelChoiceField(queryset=User.objects.all())
		role = forms.ModelChoiceField(context.roles)
	return MemberForm

def add_members(request, template_name="compass_tweets/add_members.html"):
	if not 'context' in request.session:
		raise Http404
	newcontext = request.session['context']
	MemberForm = make_member_form(newcontext)
	MemberFormSet = formset_factory(form=MemberForm, extra =10)
	if request.POST:	
		contextmemberformset = MemberFormSet(request.POST, prefix='members')
		if contextmemberformset.is_valid():
			for mf in contextmemberformset.forms:
				if not mf.cleaned_data.get('member') == None:
					newmember = mf.cleaned_data.get('member')
					newrole = mf.cleaned_data.get('role')
					memberrole, created = ContextMember.objects.get_or_create(member=newmember,role = newrole,context=newcontext)
					if not created:
						memberrole.save()
					
			del request.session['context']
			return HttpResponseRedirect(reverse('index'))
		else:
			return HttpResponse(contextmemberformset.errors)
	else:
		contextmemberformset = MemberFormSet(prefix='members')
		return render_to_response(template_name,{"contextmemberformset":contextmemberformset, "contextname":newcontext.name})

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
