from django.urls import path
from .views import ai_query_view

urlpatterns = [
    path('', ai_query_view, name='ai_query'),
]