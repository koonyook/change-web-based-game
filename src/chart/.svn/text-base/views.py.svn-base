# -*- coding: UTF-8 -*-
from newtype.chart.models import State
from django.http import HttpResponse
from newtype.helpers.http import JSONResponse

# Create your views here.
DEFAULT_LIMIT = 365

def pollutions(request):
    """docstring for pollutions"""
    limit = DEFAULT_LIMIT
    if request.REQUEST.__contains__('limit'):
        limit = request.REQUEST['limit']
    
    air_pollution = list()
    earth_pollution = list()
    water_pollution = list()
    i = 1
    for state in State.objects.all().order_by('-time')[:limit].reverse():
        air_pollution.append( [ i, state.air_pollution ] )
        water_pollution.append( [ i, state.water_pollution ] )
        earth_pollution.append( [ i, state.earth_pollution ] )
        i += 1
        
    return {
        'air_pollution': air_pollution,
        'water_pollution': water_pollution,
        'earth_pollution': earth_pollution,
    }
    
def natural_resources(request):
    """docstring for natural_resources"""
    limit = DEFAULT_LIMIT
    if request.REQUEST.__contains__('limit'):
        limit = request.REQUEST['limit']
        
    natural_resources = list()
    i = 1
    for state in State.objects.all().order_by('-time')[:limit].reverse():
        natural_resources.append( [ i, state.natural_resources ] )
        i += 1
        
    return  natural_resources 
    
def researches(request):
    """docstring for researches"""
    limit = DEFAULT_LIMIT
    if request.REQUEST.__contains__('limit'):
        limit = request.REQUEST['limit']
    
    researches = list()
    i = 1
    for state in State.objects.all().order_by('-time')[:limit].reverse():
        researches.append( [ i, state.researches ] )
        i += 1
        
    return ( researches )
    
def getall(request):
    return JSONResponse({
        'pollution': pollutions(request),
        'natural_resources': natural_resources(request),
        'researches': researches(request), 
    })