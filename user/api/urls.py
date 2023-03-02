from django.urls import path,include
from user.api import views as user_api_views
from rest_framework.authtoken.views import obtain_auth_token
from .routers import router
app_name = 'user'

urlpatterns = [
    path('register/', user_api_views.Register, name="register"),
    path('logout/', user_api_views.Logout, name="logout"),
    path('login/', user_api_views.login, name="login"),
    path('check/', user_api_views.check_unique, name="check"),
    path('password/reset/', user_api_views.forgotpassword, name='forgot'),
    path('password/confirm/', user_api_views.confirm_reset, name='confirm'),
    path('sets/', include(router.urls)),
    path('status/', user_api_views.drag_status, name='status'),
    path('profile/drag/',user_api_views.prepare_drag_profile, name='dragprofile')
    # path('profile/request/', user_api_views.DragProfileViewSet.as_view({'post':'perform_create'}), name="upload")
]

