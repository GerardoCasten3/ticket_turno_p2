from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_view, name='ticket_view'),
    path('post_ticket/', views.post_ticket, name='post_ticket'),
    path('get_ticket/<int:ticket_id>/', views.get_ticket, name='get_ticket'),
    path('search_ticket/<int:ticket_id>/', views.search_ticket, name='search_ticket'),
    path('get_edit_ticket/<int:ticket_id>/', views.get_edit_ticket, name='edit_ticket'),
    path('update_ticket/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
]
