from django.urls import path,include
from user.api import views as user_api_views
from rest_framework.authtoken.views import obtain_auth_token
from .routers import event_router
app_name = 'event'


urlpatterns = [
    path('actions/', include(event_router.urls)),
]