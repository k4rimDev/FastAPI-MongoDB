from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('akm1n/', admin.site.urls),
    path("product/", include("product.api.urls"))
]

schema_view = get_schema_view(
    openapi.Info(
        title="Qmeter task APIs",
        default_version='v0.0.1',
        description="Online health consultant",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="karimmirzaguliyev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)