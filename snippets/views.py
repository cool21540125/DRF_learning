"""
    最一開始的 API View
"""
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly

class SnippetList(generics.ListCreateAPIView):
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class UserList(generics.ListCreateAPIView):
    """
        All Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        First Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
