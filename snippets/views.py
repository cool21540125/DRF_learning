"""
    最一開始的 API View
"""
from rest_framework.views import APIView # from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetList(APIView):
    """
        all snippets
    """
    def get(self, request, format=None):
        objs = Snippet.objects.all()
        sers = SnippetSerializer(objs, many=True)
        return Response(sers.data)

    def post(self, request, format=None):
        sers = SnippetSerializer(data=request.data)
        if sers.is_valid():
            sers.save()
            return Response(sers.data, status=status.HTTP_201_CREATED)
        return Response(sers.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
        取, 刪, 改
    """
    def __get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.__get_object(pk)
        ser = SnippetSerializer(obj)
        return Response(ser.data)

    def put(self, request, pk, format=None):
        obj = self.__get_object(pk)
        ser = SnippetSerializer(obj, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.__get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
