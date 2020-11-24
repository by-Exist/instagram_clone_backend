from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import SignupSerializer, SuggestionUserSerializer


class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  # TODO: 인증 권한 제거


class SuggestionListAPIView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SuggestionUserSerializer
    permission_classes = [AllowAny]  # TODO: 인증 권한 제거

