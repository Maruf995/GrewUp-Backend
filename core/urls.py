from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Импорты для Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка внешнего вида документации
schema_view = get_schema_view(
   openapi.Info(
      title="CrewUp Demo API",
      default_version='v1',
      description="API документация для стартап-презентации",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@crewup.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Подключение твоего приложения (убедись, что имя папки верное, например 'api' или 'main')
    path('api/', include('api.urls')), 

    # --- SWAGGER URLS ---
    # По ссылке /swagger/ будет красивый интерфейс
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # По ссылке /redoc/ будет другой стиль документации (более строгий)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Раздача картинок (для аватарок и постов)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)