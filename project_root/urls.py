from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('auth_app.urls')),
    path('api/bookstore/', include('bookstore.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
    path('api/swagger/', include('project_root.swagger.urls')),
]
