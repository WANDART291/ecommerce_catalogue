from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # 1. Admin
    path('admin/', admin.site.urls),

    # 2. Catalogue API
    path('api/v1/catalogue/', include('catalogue.urls')),

    # 3. Cart API
    path('api/v1/', include('cart.urls')),

    # 4. Orders API (THIS IS THE NEW PART)
    path('api/v1/', include('orders.urls')),

    # 5. Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
   urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Authentication (Add these 2 lines) ---
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # --- Your Apps ---
    path('api/v1/catalogue/', include('catalogue.urls')),
    path('api/v1/', include('cart.urls')),
    path('api/v1/', include('orders.urls')),

    # --- Documentation ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]