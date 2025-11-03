from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_view, name='ticket_view'),
    path('post_ticket/', views.post_ticket, name='post_ticket'),
    path('get_ticket/<str:ticket_turno>/', views.get_ticket, name='get_ticket'),
    path('get_ticket_id/<int:ticket_id>/', views.get_ticket_id, name='get_ticket_id'),
    path('search_ticket/<str:ticket_turno>/', views.search_ticket, name='search_ticket'),
    path('get_edit_ticket/<str:ticket_turno>/', views.get_edit_ticket, name='edit_ticket'),
    path('update_ticket/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('login/', views.custom_login, name='custom_login'),
]
