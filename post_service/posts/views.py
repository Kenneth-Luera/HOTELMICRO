from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Post, PostImage
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')

        if role:
            queryset = queryset.filter(role=role)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        post = serializer.save(
            user_id=user.id,
            role=user.role
        )

        images = self.request.FILES.getlist('images')

        for image in images:
            PostImage.objects.create(post=post, image=image)

    def perform_update(self, serializer):
        user = self.request.user

        if str(serializer.instance.user_id) != str(user.id):
            raise PermissionDenied("No puedes editar este post")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if str(instance.user_id) != str(user.id):
            raise PermissionDenied("No puedes eliminar este post")

        instance.delete()