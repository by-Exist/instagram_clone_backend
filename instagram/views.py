from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Post, Comment
from .serializers import CommentSerializer, PostSerializer


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

    # serializer에서 context를 활용할 수 있게 이런 방식을 지원할 수 있다.
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

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

    @action(detail=True, methods=["POST"])
    def like(self, request, pk):
        post = self.get_object()
        post.like_user_set.add(self.request.user)
        return Response(status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self, request, pk):
        post = self.get_object()
        post.like_user_set.remove(self.request.user)
        return Response(status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # serializer에서 context를 활용할 수 있게 이런 방식을 지원할 수 있다.
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(post__pk=self.kwargs["post_pk"])
        return qs

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(author=self.request.user, post=post)
        return super().perform_create(serializer)

