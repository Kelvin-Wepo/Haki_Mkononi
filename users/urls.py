from django.urls import path
from . import views
from .views import login_view
from .views import dashboard_view 
from django.contrib.auth.views import LogoutView 
from .views import edit_profile

urlpatterns = [
    path('register/', views.register, name='register'),  
     path('login/', login_view, name='login'),
    path('profile/', views.profile, name='profile'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
     path('logout/', LogoutView.as_view(), name='logout')
]

