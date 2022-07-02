from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse
from . import RSFunction


@api_view(['GET'])
def getData(request, username):
    player = RSFunction.GetPlayerData(name=username)
    return Response(player)

@api_view(['GET'])
def updateData(request, username):
    player = RSFunction.UpdatePlayerData(name=username)
    return Response(player)

def home(request):
    return HttpResponse('<h1>API Home</h1>')