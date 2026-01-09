from django.db.models import Q, ObjectDoesNotExist
from rest_framework import serializers
from .models import Point, Message
from users.models import Raider
from django.contrib.gis.db.models.fields import Point as PointField


class PointSerializer(serializers.ModelSerializer):
    """Сериализатор модели Точки"""

    def validate_location(self, value):
        """Принимаем на вход список из двух позиций, а возвращаем экземпляр класса
        Point из django.contrib.gis.db.models.fields (не путать с нашим собственным классом Point."""
        try:
            lat, lon = value
        except ValueError:
            raise serializers.ValidationError(detail="Ошибка при вводе координат. Передайте ровно два значения.")
        else:
            return PointField(x=lat, y=lon, srid=4326)

    class Meta:
        model = Point
        fields = ['id', 'title', 'location']


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор модели Сообщения"""
    point = serializers.StringRelatedField(read_only=True, label='Точка')
    user = serializers.StringRelatedField(read_only=True, label='Искатель')
    time_create = serializers.DateTimeField(format='%d.%m.%Y %H:%M', label='Дата и время сообщения')
    text_content = serializers.CharField(label='Сообщение')

    class Meta:
        model = Message
        fields = ['point', 'text_content', 'user', 'time_create']
