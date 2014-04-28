from django.contrib import admin
from compass_tweets.models import Context,Type,Role,Rule,CTweet,ContextMember

class TypeInline(admin.StackedInline):
	model = Type
	extra = 3
	
class RoleInline(admin.StackedInline):
	model = Role
	extra = 3
	
class RuleInline(admin.TabularInline):
	model = Rule
	extra = 2


class ContextAdmin(admin.ModelAdmin):
	fields = ['name']
	inlines = [TypeInline,RoleInline,RuleInline]

admin.site.register(Context,ContextAdmin)
admin.site.register(CTweet)
admin.site.register(ContextMember)

