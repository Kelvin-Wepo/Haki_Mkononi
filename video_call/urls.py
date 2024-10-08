from django.urls import path
from . import views

urlpatterns = [
    path('video-call/initiate/<int:official_id>/', views.initiate_call, name='initiate_call'),
    path('join/<str:room_name>/', views.join_call, name='join_call'),
    path('history/', views.call_history, name='call_history'),
]
