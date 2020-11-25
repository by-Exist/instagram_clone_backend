from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = (
        # Post List API에서 SQL 요청을 보며 반복되는 WHERE에 집중한다.
        # Post : 1로 표현, select_related => accounts_user에 해당
        # Post : N으로 표현, prefetch_related => teg_set, like_user_set에 해당
        Post.objects.all()
        .select_related("author")
        .prefetch_related("tag_set", "like_user_set")
        # 쿼리 속도/갯수가 9.00ms/22개에서 5.00ms/9개로 줄어들었다.
    )
    serializer_class = PostSerializer

    def get_queryset(self):
        time_since = timezone.now() - timedelta(days=3)
        qs = super().get_queryset()
        login_user = self.request.user
        qs = qs.filter(
            Q(author=login_user) | Q(author__in=login_user.following_set.all())
        ).filter(created_at__gte=time_since)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)
