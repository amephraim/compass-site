from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes import generic


class Type(models.Model):
	name = models.CharField(max_length=50, verbose_name='type_name')
	def __unicode__(self):
		return u"%s" % (self.name) 

class Role(models.Model): 
    name = models.CharField(max_length=50,verbose_name='role_name')
    def __unicode__(self):
		return u"%s" % (self.name)
		
class Rule(models.Model):
	message_type = models.ForeignKey(Type,related_name='message_type')
	sender_role = models.ForeignKey(Role, related_name='sender_name')
	receiver_role = models.ForeignKey(Role, related_name='receiver_name')
	def __unicode__(self):
		return u"Sender %s Receiver %s Type %s" % (self.sender_role,self.receiver_role,self.message_type)
		
class Context(models.Model):
    name = models.CharField(max_length=50)
    types = models.ManyToManyField(Type)
    roles = models.ManyToManyField(Role)
    rules = models.ManyToManyField(Rule)
    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey('owner_type', 'owner_id')

    def __unicode__(self):
        return u"%s" % (self.name)    

	
class CTweet(models.Model):
	message = models.CharField(max_length=500)
	sender = models.CharField(max_length = 50)
	receiver = models.CharField(max_length = 50)
	message_type = models.ForeignKey(Type,related_name ='cTweet_type')
	context = models.ForeignKey(Context,related_name='cTweetContext')
	subject = models.CharField(max_length = 50)

class ContextFriendshipManager(models.Manager):
	def remove (self,user1, user2):
		if self.filter(from_user=user1, to_user=user2):
			contextfriendship = self.filter(from_user=user1, to_user=user2)
		contextfriendship.delete()

class ContextFriendship(models.Model):
	from_user = models.ForeignKey(User,related_name="me",editable=False)
	to_user = models.ForeignKey(User, related_name="__myfriend__",editable=False)
	relationship=models.ForeignKey(ContentType)
	objects=ContextFriendshipManager()
	class Meta:
		unique_together= (('from_user','to_user'),)

class FriendRelations(models.Model):
	relation_name=models.CharField(max_length=50)

def contextfriend_set_for(user):
    return set([obj["contextfriend"] for obj in ContextFriendship.objects.contextfriends_for_user(user)])


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
