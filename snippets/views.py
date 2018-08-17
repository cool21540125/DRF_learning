"""
    最一開始的 API View
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
        List 所有 code snippets / create
    """
    if request.method == 'GET':
        objs = Snippet.objects.all()
        sers = SnippetSerializer(objs, many=True)
        return Response(sers.data)

    if request.method == 'POST':
        sers = SnippetSerializer(data=request.data)
        if sers.is_valid():
            sers.save()
            return Response(sers.data, status=status.HTTP_201_CREATED)
        return Response(sers.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
        取, 刪, 改
    """
    try:
        obj = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = SnippetSerializer(obj)
        return Response(ser.data)

    if request.method == 'PUT':
        ser = SnippetSerializer(obj, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
