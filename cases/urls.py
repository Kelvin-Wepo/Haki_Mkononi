from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('search/', views.case_search, name='case_search'),
    path('create-case/', views.create_case, name='create_case'), 
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('cases/', views.case_list, name='case_list'),
]