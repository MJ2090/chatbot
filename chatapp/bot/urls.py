from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('test/', views.test, name='test'),
    path('test_json/', views.test_json, name='test_json'),
]

urlpatterns += staticfiles_urlpatterns()