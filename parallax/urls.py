from django.contrib import admin
from django.urls import path

import django_cas_ng.views as cas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login', cas_views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
]
