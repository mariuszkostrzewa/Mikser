from django.http import HttpResponse
from django.template import loader
from .models import Pomiar

def index(request):
    latest_results=Pomiar.objects.order_by('-pub_date')[:5]
    template=loader.get_template('konsola/index.html')
    context={
        'latest_results':latest_results,
        }
    return HttpResponse(template.render(context, request))