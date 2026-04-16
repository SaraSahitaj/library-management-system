from django.contrib import admin
from django.urls import include, path
from books.views import home_view, dashboard_view
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('ai-query/', include('ai_assistant.urls')),
]
