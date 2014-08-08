from django import template
from compass_tweets.forms import ContextForm

register = template.Library()


@register.inclusion_tag("compass_tweets/compass_item.html", takes_context=True)
def show_context(context, contxt):
    print contxt.name
    return {'ContextTemplate': contxt, 'request': context['request']}

# @@@ should move these next two as they aren't particularly tribe-specific

@register.simple_tag
def clear_search_url(request):
    getvars = request.GET.copy()
    if 'search' in getvars:
        del getvars['search']
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path


@register.simple_tag
def persist_getvars(request):
    getvars = request.GET.copy()
    if len(getvars.keys()) > 0:
        return "?%s" % getvars.urlencode()
    return ''
