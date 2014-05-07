from django import forms
from compass_tweets.models import Context, Role, Type, Rule
from django.forms.models import inlineformset_factory, modelformset_factory

try:
	from notification import models as notification
except ImportError:
    notification = None
    
MAX_ENTITIES = 3

class TypeForm(forms.ModelForm):
	class Meta :
		model = Type

class RoleForm(forms.ModelForm):
	class Meta :
		model = Role

class RuleForm(forms.ModelForm):
	class Meta :
		model = Rule
		
class ContextForm(forms.ModelForm):
	
	class Meta :
		model = Context
		exclude = ('owner_type','owner_id','owner')
		
	def __init__(self, user=None, *args, **kwargs):
		self.user = user # get user here!
		super(ContextForm, self).__init__(*args, **kwargs) #creates an object of type ModelForm. inheritance basically.
	
	def save(self,commit = True):
		new_context = super(ContextForm,self).save(commit=False)
		new_context.owner = self.user
		if commit:
			new_context.save()
		return new_context




