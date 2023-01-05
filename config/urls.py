from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from hotel_manager.users.api.auth_view import MyTokenObtainPairView, LogoutView
from hotel_manager.users.api.views import RegisterView, RegisterCustomerView
from hotel_manager.facebook.api.facebook_auth_view import FacebookWebhookView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("api/register-staff/", RegisterView.as_view(), name='register-staff'),
    path("api/sign-up/", RegisterCustomerView.as_view(), name='sign-up'),
    path("chat/receiver/", FacebookWebhookView.as_view(), name='webhook-fb'),
    # path("chat/receiver", VerifyFacebookWebhookView.as_view(), name='webhook-fb-get'),
    path("users/", include("hotel_manager.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path('tinymce/', include('tinymce.urls')),
    path("api/login/", TokenObtainPairView.as_view(), name='login'),
    # path("api/login/", MyTokenObtainPairView.as_view(), name='login'),
    path("api/logout/", LogoutView.as_view(), name='logout'),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
