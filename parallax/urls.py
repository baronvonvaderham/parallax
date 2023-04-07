from django.contrib import admin
from django.urls import path

import django_cas_ng.views as cas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^accounts/login$', cas_views.login, name='cas_ng_login'),
    path(r'^accounts/logout$', cas_views.logout, name='cas_ng_logout'),
    path(r'^accounts/callback$', cas_views.views.callback, name='cas_ng_proxy_callback'),
]
