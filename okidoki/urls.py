from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('work/', include('work.urls')),
    path('', include('main.urls'))
]

urlpatterns += staticfiles_urlpatterns()