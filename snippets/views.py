"""
    最一開始的 API View
"""
from rest_framework import generics
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetList(generics.ListCreateAPIView):
    """
        all snippets
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        取, 刪, 改
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
