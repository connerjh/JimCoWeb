from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('portal/', include('portal.urls')),
    path('admin/', admin.site.urls)
]
