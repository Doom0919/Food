from django.contrib import admin
from django.urls import path, include
import core

# Төслийн нэрээр биш, апп-ын нэрээр шууд дуудна (..core биш core)

urlpatterns = [
    # Admin-аас гадуур байгаа тул 403 алдаа гарахгүй
    path('api/', include('core.urls')),
    path('', admin.site.urls),
]