# Create your views here.
from django.http import HttpResponse
    
def newsfeed(request):
	return HttpResponse("Compass newsfeed ")
	
def contextdef(request):
	return HttpResponse("Compass context definitions")

def index(request):
    return HttpResponse("Hello, world. You're at Compass")
