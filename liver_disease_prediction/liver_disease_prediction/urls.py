from django.contrib import admin
from django.urls import path
from Remote_User import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login, name='login'),
    path('register/', views.Register1, name='register'),

    path('profile/', views.ViewYourProfile, name='ViewYourProfile'),

    path('predict/', views.Predict_Liver_Disease_Status,
         name='Predict_Liver_Disease_Status'),
]
