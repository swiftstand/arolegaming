"""drag4me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import home_page, register, web_profile, display_qr, web_save_qr, web_login, payment_webhook, callback_endpoint, web_logout, web_request_reset, web_complete_password_reset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="index"),
    path('web/register/', register, name="web_register"),
    path('web/login/', web_login, name="web_login"),
    path('web/logout/', web_logout, name="web_logout"),
    path('web/profile/', web_profile, name="web_profile"),
    path('web/qr/', display_qr, name="display_qr"),
    path('web/save/', web_save_qr, name="web_save_qr"),
    path('arole/pay/webhook/', payment_webhook, name="web_hook"),
    path('arole/callback/', callback_endpoint, name='deliver_value'),
    path('arole/reset/', web_request_reset, name='web_request_reset'),
    path('arole/confirm/', web_complete_password_reset, name='web_confirm_reset'),

    #REST FRAMEWORK
    path('api/user/', include('user.api.urls',)),
    path('api/event/', include('event.api.urls',)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

