from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

def Home(request):
    context = {}
    return render_to_response('base.html', context, context_instance=RequestContext(request))
