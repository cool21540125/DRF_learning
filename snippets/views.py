"""
    最一開始的 API View
"""
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@csrf_exempt
def snippet_list(request):
    """
        List 所有 code snippets / create
    """
    if request.method == 'GET':
        objs = Snippet.objects.all()
        sers = SnippetSerializer(objs, many=True)
        return JsonResponse(sers.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        sers = SnippetSerializer(data=data)
        if sers.is_valid():
            sers.save()
            return JsonResponse(sers.data, status=201)
        return JsonResponse(sers.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
        取, 刪, 改
    """
    try:
        obj = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        ser = SnippetSerializer(obj)
        return JsonResponse(ser.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        ser = SnippetSerializer(obj, data=data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data)
        return JsonResponse(ser.errors, status=400)

    if request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)
