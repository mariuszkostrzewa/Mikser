from django.http import HttpResponse
from django.template import loader
from .models import Read

# from highcharts.views import HighChartsBarView
from random import random
from multiprocessing.sharedctypes import template
from django.template.context_processors import request
from konsola.xrangeData import XRangeData
from konsola.reads import Reads
import json

def index(request):
    latest_results=Read.objects.order_by('-pub_date')[:5]
    template=loader.get_template('konsola/index.html')
    context={
        'latest_results':latest_results,
        }
    return HttpResponse(template.render(context, request))

def xrange(request):
    
    template=loader.get_template('konsola/xrange.html')
    context={}
    return HttpResponse(template.render(context, request))

def xrange_json(request):
    data=XRangeData.get_xRangeData()
    return HttpResponse(json.dumps(data), content_type='application/json')
 
def reads(request):
    
    template=loader.get_template('konsola/reads.html')
    context={}
    return HttpResponse(template.render(context, request))

def reads_json(request):
    data=Reads.getJson()
    return HttpResponse(json.dumps(data), content_type='application/json')