from django.urls import path


from .views import submitData

app_name="rest_api"

urlpatterns = [
    path('submitData/', submitData)
]

