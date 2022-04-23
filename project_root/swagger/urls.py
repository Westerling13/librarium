from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='swagger_schema'), name='swagger_ui'),
    path('schema/', SpectacularAPIView.as_view(), name='swagger_schema'),
]
