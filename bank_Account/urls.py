from django.urls import include, path
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view
from rest_framework.permissions import IsAdminUser

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Простая реализация банковских транзакций",
        default_version="v1",
        description="Этот проект представляет собой простую реализацию API для управления банковскими транзакциями. Включены интерфейсы для создания, перечисления и извлечения банковских счетов, а также для перевода денег между счетами, а также для дебетования и зачисления средств на счет.",
        terms_of_service="https://policies.google.com/",
        contact=openapi.Contact(
            name = "Marselle Naz",
            url = "https://t.me/MarselleNaz",
            email = "marselle.naz@yandex.kz",
        ),
        license=openapi.License(
            name = "MIT",
            url = "https://opensource.org/license/mit",
        )
    ),
    public=True,
    permission_classes=[IsAdminUser],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-token-auth/', obtain_jwt_token),
    path('auth-token-refresh/',refresh_jwt_token),
    path('auth-token-verify/', verify_jwt_token),
]
