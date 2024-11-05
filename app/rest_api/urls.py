from django.urls import path


from .views import submitData, getedit_pereval

app_name="rest_api"

urlpatterns = [
    path('submitData/', submitData, name='submitData'),
    path('submitData/<int:pk>', getedit_pereval, name='submitDataPK')
]

