from django.urls import path

from . import views
from ctypes.test.test_pickling import name

urlpatterns = [
    path('', views.index, name='index'),
    path('xrange', views.xrange, name='xrange'),
    path('xrange_json', views.xrange_json, name='xrange_json'),
    path('reads', views.reads, name='reads'),
    path('reads_json', views.reads_json, name='reads_json')
]