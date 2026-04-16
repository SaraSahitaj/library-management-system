from django.urls import path
from .views import library_insights
from . import views

from .views import (
    book_create_view,
    book_delete_view,
    book_list_view,
    book_update_view,
)

urlpatterns = [
    path('', book_list_view, name='book_list'),
    path('add/', book_create_view, name='book_add'),
    path('<int:pk>/edit/', book_update_view, name='book_edit'),
    path('<int:pk>/delete/', book_delete_view, name='book_delete'),
    path('insights/', library_insights, name='library_insights'),

]
