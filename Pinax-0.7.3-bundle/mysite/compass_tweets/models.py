from django.db import models

from microblogging.models import Tweet

class Context(models.Model):
    name = models.CharField(max_length=50)
#    class Meta:
#        app_label='test
    def __unicode__(self):
        return u"%s" % (self.name)    

class Type(models.Model):
    context = models.ForeignKey(Context)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s %s" % (self.name,self.context)    
#    class Meta:
#        app_label='test'
        
class Role(models.Model):
    context = models.ForeignKey(Context)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return u"%s %s" % (self.name,self.context)
#    class Meta:
#        app_label='test'

class Rule(models.Model):    
    context = models.ForeignKey(Context,related_name='context')
    message_type = models.ForeignKey(Type,related_name='message_type')
    sender_role = models.ForeignKey(Role, related_name='sender_name')
    receiver_role = models.ForeignKey(Role, related_name='receiver_name')
    bool_send = models.BooleanField(default=False)
#    class Meta:
#        app_label='test'
# add field for tweet instances?
