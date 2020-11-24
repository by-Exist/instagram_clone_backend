from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        time_since = timezone.now() - timedelta(days=3)
        qs = super().get_queryset()
        login_user = self.request.user
        qs = qs.filter(
            Q(author=login_user) | Q(author__in=login_user.following_set.all())
        ).filter(created_at__gte=time_since)
        return qs
