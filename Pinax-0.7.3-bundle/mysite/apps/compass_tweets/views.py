from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from compass_tweets.models import Context,Type, Role, Rule
from compass_tweets.forms import ContextForm,TypeFormSet, RoleFormSet, RuleFormSet
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def add_context(request,template_name = "compass_tweets/editcontext.html"):
	if request.POST:
		form = ContextForm(request.user,request.POST)
		if form.is_valid():
			print request.POST
			context = form.save(commit=False)
			print request.user
			type_formset = TypeFormSet(request.POST, instance = context)
			role_formset = RoleFormSet(request.POST, instance = context)
			rule_formset = RuleFormSet(request.POST, instance = context)
			if type_formset.is_valid() and role_formset.is_valid() and rule_formset.is_valid():
				context.save()
				type_formset.save()
				role_formset.save()
				rule_formset.save()
				return HttpResponseRedirect('Entry made')
	else:
		form = ContextForm()
		type_formset = TypeFormSet(instance = Context())
		role_formset = RoleFormSet(instance = Context())
		rule_formset = RuleFormSet(instance = Context())
		return render_to_response(template_name,{
			"form": form, "type_formset":type_formset,"role_formset":role_formset,"rule_formset":rule_formset, })

'''
def add_context(request, template_name="compass_tweets/editcontext.html"):
	#return HttpResponse("Adding contexts!!!!!!!!!! - not really my love")
	if request.method == "POST":
		cform = ContextForm(request.POST, instance=Context())
        typeforms = [TypeForm(request.POST, prefix=str(x), instance=Type()) for x in range(0,2)]
        roleforms = [RoleForm(request.POST, prefix=str(x), instance=Role()) for x in range(0,2)]
        ruleforms = [RuleForm(request.POST, prefix=str(x), instance=Rule()) for x in range(0,2)]
        
        if cform.is_valid() and all([tf.is_valid() for tf in typeforms]) and all([rf.is_valid() for rf in ruleforms])and all([rf.is_valid() for rf in roleforms]):
			new_context = cform.save()
			for tf in typeforms:
				new_type = tf.save(commit=False)
				new_type.context = new_context
				new_type.save()
			for rf in roleforms:
				new_role = rf.save(commit=False)
				new_role.context = new_context
				new_role.save()
			for rf in ruleforms:
				new_rule = rf.save(commit=False)
				new_rule.context = new_context
				new_rule.save()
			return HttpResponseRedirect('/context/add/')
	else:
			
		cform = ContextForm(instance=Context())
		roleforms = [RoleForm(prefix=str(x), instance=Role()) for x in range(0,2)]
		ruleforms = [RuleForm(prefix=str(x), instance=Rule()) for x in range(0,2)]
		typeforms = [TypeForm(prefix=str(x), instance=Type()) for x in range(0,2)]
		
		return render_to_response(template_name, {'context_form': cform, 'role_forms': rforms})
add_context=login_required(add_context)
'''

def newsfeed(request):
	return HttpResponse("Compass newsfeed ")
	
def contextdef(request):
	return HttpResponse("Compass context definitions")

def index(request):
    return HttpResponse("Hello, world. You're at Compass")
