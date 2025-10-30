"""Senacmon URL configuration."""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls', "accounts"), name='accounts'),
    path('game/', include('game.urls', "game"), name='game'),
    path('wallet/', include('wallet.urls', "wallet"), name='wallet'),
]
