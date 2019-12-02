from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from logging import debug

def JSONResponse(raw_data, force_serialize_as_objects=False):
    """serialized raw_data and return HttpResponse object"""
    content_type = 'application/javascript; charset=utf8'
    
    if not force_serialize_as_objects:
        allowed_type = [type(dict()), type(list()), type(unicode())]
        if type(raw_data) in allowed_type:
            return HttpResponse( simplejson.dumps(raw_data), content_type=content_type)
            
    return HttpResponse(serializers.serialize('json', raw_data, ensure_ascii=False), content_type=content_type)
    
# from django.core.serializers import json, serialize
# from django.db.models.query import QuerySet
# from django.http import HttpResponse
# from django.utils import simplejson
# 
# class JsonResponse(HttpResponse):
#     def __init__(self, object):
#         if isinstance(object, QuerySet):
#             content = serialize('json', object)
#         else:
#             content = simplejson.dumps(
#                 object, indent=2, cls=json.DjangoJSONEncoder,
#                 ensure_ascii=False)
#         super(JsonResponse, self).__init__(
#             content, content_type='application/json')
