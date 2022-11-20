from django.urls import include, path
from rest_framework import routers

from .views import UploadViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"upload-image", UploadViewSet, basename="upload")

urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
