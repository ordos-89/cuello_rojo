from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, renderer_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.db.models.functions import Distance
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.db.models.fields import Point as DjangoPoint
from django.views.decorators.csrf import csrf_protect

from .serializers import PointSerializer, MessageSerializer
from .models import Point


@authentication_classes([SessionAuthentication, BasicAuthentication])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_points(request):
    """Функционал: создание точки на карте"""

    if request.method == "POST":
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(left_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if request.data:
            lat = request.data.get('latitude', 0)
            lon = request.data.get('longitude', 0)
            radius = request.data.get('radius', 0)

            search_center_location = DjangoPoint(x=lat, y=lon, srid=4326)

            points = Point.objects.annotate(distance=Distance('location',
                                                              search_center_location)
                                            ).filter(distance__lte=radius).order_by('-distance')
        else:
            # Для целей тестирования (ручного). Можно получить список всех точек, обратившись по адресу "api/points/".
            points = Point.objects.all()

        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_messages(request):
    """Функционал: добавление сообщений к точке"""

    if request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Автор сообщения - авторизованный пользователь. Берём из запроса.
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
