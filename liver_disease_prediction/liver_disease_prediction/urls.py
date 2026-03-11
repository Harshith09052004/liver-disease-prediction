from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from Remote_User import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('predict/', views.predict),
]
