from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from library import views

urlpatterns = [
    path('list/', views.LibraryListView.as_view(), name='library-list')
]

urlpatterns = format_suffix_patterns(urlpatterns)
