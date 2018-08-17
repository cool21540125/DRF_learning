"""
    最一開始的 API View
"""
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer


class SnippetList(generics.ListAPIView):
    """
        all snippets
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveAPIView):
    """
        取, 刪, 改
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class UserList(generics.ListAPIView):
    """
        All Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
        First Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
