import django.db.models
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.db.models.functions import Distance
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.db.models.fields import Point as DjangoPoint

from .serializers import PointSerializer, MessageSerializer
from .models import Point, Message


def get_points_in_area(lat: float or int, lon: float or int, radius: float or int) -> django.db.models.QuerySet:
    """Поиск точек в радиусе от заданного центра. Возвращаем набор этих точек (queryset)
    Данный функционал используется как при поиске самих точек, так и при поиске сообщений в заданной географии."""
    search_center_location = DjangoPoint(x=lat, y=lon, srid=4326)

    points = Point.objects.annotate(distance=Distance('location',
                                                      search_center_location)
                                    ).filter(distance__lte=radius).order_by('-distance')
    return points


@authentication_classes([SessionAuthentication, BasicAuthentication])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_points(request):
    """Функция для работы с точками. Просмотр точек в заданном радиусе, добавление точек."""

    if request.method == "POST":
        # добавление точки
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(left_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Поиск точек в радиусе от заданной точки
        if request.data:
            lat = request.data.get('latitude', 0)
            lon = request.data.get('longitude', 0)
            radius = request.data.get('radius', 0)

            points = get_points_in_area(lat, lon, radius)

        else:
            # Для целей тестирования (ручного). Можно получить список всех точек, обратившись по адресу "api/points/".
            points = Point.objects.all()

        serializer = PointSerializer(points, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_messages(request):
    """Работа с сообщениями. Добавление сообщений к заданной точке, поиск сообщений в радиусе."""

    if request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Автор сообщения - авторизованный пользователь. Берём из запроса.
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Поиск сообщений в радиусе от заданных координат

        if request.data:
            # Если переданы координаты и радиус, ищем с учётом этих данных
            lat = request.data.get('latitude', 0)
            lon = request.data.get('longitude', 0)
            radius = request.data.get('radius', 0)
            points = get_points_in_area(lat, lon, radius).values_list("pk", flat=True)
            messages = Message.objects.filter(point__pk__in=points)

        else:
            messages = Message.objects.all()

        serializer = MessageSerializer(messages, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
