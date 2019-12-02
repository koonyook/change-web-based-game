# -*- coding: UTF-8 -*-
from newtype.core.models import Player, Union, ResearchLog
from newtype.patent.models import Patent
from django.db.models import Count
from datetime import datetime
# from django.http import HttpResponseRedirect, HttpResponse
from newtype.helpers.http import JSONResponse

# Create your views here.

# Players related
def players_max_money(request, limit):
    """docstring for players_max_money"""
    players = Player.objects.all().order_by('-money')[:limit]
    ret = dict()
    ret['head1'] = u'ผู้เล่น'
    ret['head2'] = u'เงิน'
    response = list()
    for player in players:
        each_player = dict()
        each_player['name'] = player.user.username
        each_player['data'] = player.money
        response.append(each_player)
    ret['data'] = response
    return JSONResponse(ret)
    
def players_most_research(request, limit):
    """docstring for players_most_research(request, limit"""
    players = Player.objects.annotate(Count('researchlog')).all().order_by('-researchlog__count')[:limit]
    ret = dict()
    ret['head1'] = u'ผู้เล่น'
    ret['head2'] = u'วิจัย'
    response = list()
    for player in players:
        each_player = dict()
        each_player['name'] = player.user.username
        each_player['data'] = ResearchLog.objects.filter(player=player).count()
        response.append(each_player)
    ret['data'] = response
    return JSONResponse(ret)
    
def players_most_found_patent(request, limit):
    """docstring for players_most_found"""
    players = Player.objects.annotate(Count('patent_found')).all().order_by('-patent_found__count')[:limit]
    ret = dict()
    ret['head1'] = u'ผู้เล่น'
    ret['head2'] = u'ค้นพบ'
    response = list()
    for player in players:
        each_player = dict()
        each_player['name'] = player.user.username
        each_player['data'] = Patent.objects.filter(founder=player).count()
        response.append(each_player)
    ret['data'] = response
    return JSONResponse(ret)
    
def players_most_regis_patent(request, limit):
    """docstring for players_most_own_patent"""
    players = Player.objects.annotate(Count('patent_regis')).all().order_by('-patent_regis__count')[:limit]
    ret = dict()
    ret['head1'] = u'ผู้เล่น'
    ret['head2'] = u'จดสิทธิบัตร'
    response = list()
    for player in players:
        each_player = dict()
        each_player['name'] = player.user.username
        each_player['data'] = Patent.objects.filter(player=player).count()
        response.append(each_player)
    ret['data'] = response
    return JSONResponse(ret)
    
# Union related
def unions_max_money(request, limit):
    """docstring for players_max_money"""
    unions = Union.objects.all().order_by('-money')[:limit]
    ret = dict()
    ret['head1'] = u'บริษัท'
    ret['head2'] = u'เงิน'
    response = list()
    for union in unions:
        each_union = dict()
        each_union['name'] = union.name
        each_union['data'] = union.money
        response.append(each_union)
    ret['data'] = response
    return JSONResponse(ret)
    
def unions_most_research(request, limit):
    """docstring for players_most_research(request, limit"""
    unions = Union.objects.annotate(Count('researchlog')).all().order_by('-researchlog__count')[:limit]
    ret = dict()
    ret['head1'] = u'บริษัท'
    ret['head2'] = u'วิจัย'
    response = list()
    for union in unions:
        each_union = dict()
        each_union['name'] = union.name
        each_union['data'] = ResearchLog.objects.filter(union=union).count()
        response.append(each_union)
    ret['data'] = response
    return JSONResponse(ret)
    
def unions_most_regis_patent(request, limit):
    """docstring for players_most_own_patent"""
    unions = Union.objects.annotate(Count('patent_regis')).all().order_by('-patent_regis__count')[:limit]
    ret = dict()
    ret['head1'] = u'บริษัท'
    ret['head2'] = u'จดสิทธิบัตร'
    response = list()
    for union in unions:
        each_union = dict()
        each_union['name'] = union.name
        each_union['data'] = Patent.objects.filter(union=union).count()
        response.append(each_union)
    ret['data'] = response
    return JSONResponse(ret)
    