from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("verEmail/<str:code>", verEmail, name="verEmail"),
    path('signature/<int:id>', signatureDoc, name='signatureTemplate'),
    path('viewSignature/<int:id>', view, name='viewSignature'),
    path('editTemplate/<int:id>', editDoc, name='editTemplate'),
    path('newDoc/<int:id>', newDoc, name='newDoc'),
    path("template/download/<str:id>", downloadTemplate, name="templateDownload"),
    path("signature/download/<str:id>", downloadSignature, name="signatureeDownload"),
    path('<str:page>/<str:message>', work, name='work'),
    path('<str:page>', work, name='work')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
         document_root=settings.MEDIA_ROOT)