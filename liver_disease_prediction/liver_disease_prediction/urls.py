from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from liver_disease_prediction.Remote_User import views as remoteuser
from liver_disease_prediction.Service_Provider import views as serviceprovider


urlpatterns = [
    path('admin/', admin.site.urls),

    # Remote user
    path('', remoteuser.login, name="login"),
    path('Register1/', remoteuser.Register1, name="Register1"),
    path('Predict_Liver_Disease_Status/', remoteuser.Predict_Liver_Disease_Status, name="Predict_Liver_Disease_Status"),
    path('ViewYourProfile/', remoteuser.ViewYourProfile, name="ViewYourProfile"),

    # Service provider
    path('serviceproviderlogin/', serviceprovider.serviceproviderlogin, name="serviceproviderlogin"),
    path('View_Remote_Users/', serviceprovider.View_Remote_Users, name="View_Remote_Users"),

    re_path(r'^charts/(?P<chart_type>\w+)/$', serviceprovider.charts, name="charts"),
    re_path(r'^charts1/(?P<chart_type>\w+)/$', serviceprovider.charts1, name="charts1"),
    re_path(r'^likeschart/(?P<like_chart>\w+)/$', serviceprovider.likeschart, name="likeschart"),

    path('Find_Liver_Disease_Ratio/', serviceprovider.Find_Liver_Disease_Ratio, name="Find_Liver_Disease_Ratio"),
    path('Train_Test_DataSets/', serviceprovider.Train_Test_DataSets, name="Train_Test_DataSets"),
    path('View_Liver_Disease_Status/', serviceprovider.View_Liver_Disease_Status, name="View_Liver_Disease_Status"),
    path('Download_Trained_DataSets/', serviceprovider.Download_Trained_DataSets, name="Download_Trained_DataSets"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
