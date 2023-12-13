from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import UserLoginView
from .views import UserRegistrationView

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]

