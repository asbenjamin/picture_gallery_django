import cloudinary.uploader
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Photo
from .serializers import UploadSerializer


class UploadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadSerializer

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)

    def create(self, request):
        picture = request.FILES.get("picture")
        upload_data = cloudinary.uploader.upload(picture)

        if data := upload_data:
            Photo.objects.create(
                title=request.data.get("title"),
                description=request.data.get("description"),
                image_url=data["secure_url"],
                owner=self.request.user,
            )

        return Response(
            {
                "status": "success",
                "data": upload_data,
            },
            status=201,
        )
