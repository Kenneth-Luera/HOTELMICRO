from rest_framework import viewsets
from .models import Post, PostImage
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # 🔍 Filtrar por rol (para frontend: hotel / user)
    def get_queryset(self):
        queryset = super().get_queryset()

        role = self.request.query_params.get('role')

        if role:
            queryset = queryset.filter(role=role)

        return queryset

    # 🔥 Crear post + imágenes
    def perform_create(self, serializer):
        token = self.request.auth

        post = serializer.save(
            user_id=token.get("user_id"),
            role=token.get("role")
        )

        # 📸 múltiples imágenes
        images = self.request.FILES.getlist('images')

        for image in images:
            PostImage.objects.create(post=post, image=image)

    # 🔥 (opcional) evitar que otros editen posts que no son suyos
    def perform_update(self, serializer):
        token = self.request.auth

        if str(serializer.instance.user_id) != str(token.get("user_id")):
            raise PermissionError("No puedes editar este post")

        serializer.save()

    def perform_destroy(self, instance):
        token = self.request.auth

        if str(instance.user_id) != str(token.get("user_id")):
            raise PermissionError("No puedes eliminar este post")

        instance.delete()