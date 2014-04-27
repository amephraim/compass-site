from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes import generic

class Context(models.Model):
    name = models.CharField(max_length=50)
    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('sender_type', 'sender_id')

    def __unicode__(self):
        return u"%s" % (self.name)    

class Type(models.Model):
	context = models.ForeignKey(Context, related_name = 'type_context')
	name = models.CharField(max_length=50)
        
class Role(models.Model):
    context = models.ForeignKey(Context, related_name = 'rol_context')
    name = models.CharField(max_length=50)

class Rule(models.Model):
	context = models.ForeignKey(Context)
	message_type = models.ForeignKey(Type,related_name='rule_type')
	sender_role = models.ForeignKey(Role, related_name='sender_name')
	receiver_role = models.ForeignKey(Role, related_name='receiver_name')
#	bool_send = models.BooleanField(default=False)
	
class CTweet(models.Model):
	message = models.CharField(max_length=500)
	sender = models.CharField(max_length = 50)
	receiver = models.CharField(max_length = 50)
	message_type = models.ForeignKey(Type,related_name ='cTweet_type')
	context = models.ForeignKey(Context,related_name='cTweetContext')
	subject = models.CharField(max_length = 50)

class ContextMember(models.Model):
	member_type = models.ForeignKey(ContentType)
	member_id = models.PositiveIntegerField()
	member = generic.GenericForeignKey('member_type', 'member_id')
	context = models.ForeignKey(Context,related_name='memberContext')
	role = models.ForeignKey(Role, related_name='memberRole')

def createContextInImage(contextTemplate, contextname, user):
	context_instance = Context.objects.create(name = contextname, owner=user)
	for role in Role.objects.filter(context=contextTemplate):
		role_instance = Role.objects.create(context=context_instance, name=role.name)
	for messagetype in Type.objects.filter(context=contextTemplate):
		messagetype_instance = Type.objects.create(context=context_instance, name = messagetype.name)
	for rule in Rule.objects.filter(context=contextTemplate):
		rule_instance = Rule.objects.create(context=context_instance, 
		message_type=rule.message_type, sender_role=rule.sender_role, receiver_role = rule.receiver_role)
