from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views


schema_view = get_schema_view(
    openapi.Info(title="DRF-news API", default_version="v1", description="Docs",),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
router.register("posts", views.PostViewSet)
router.register("comments", views.CommentViewSet)


urlpatterns = [
    path(
        "swagger(<format>\.json|\.yaml)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc",),
    path("", include(router.urls)),
]
