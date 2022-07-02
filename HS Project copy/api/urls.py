from django.urls import path
from . import views

urlpatterns = [
    path('player=<str:username>',views.getData),
    path('updateplayer=<str:username>', views.updateData),
    path('', views.home, name='api-home'),
]