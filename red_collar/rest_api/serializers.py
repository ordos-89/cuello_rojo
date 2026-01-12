from rest_framework import serializers
from .models import Point, Message
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
    point = serializers.PrimaryKeyRelatedField(queryset=Point.objects.all(), label='Точка')
    user = serializers.StringRelatedField(read_only=True, label='Искатель', required=False)
    time_create = serializers.DateTimeField(format='%d.%m.%Y %H:%M', label='Дата и время сообщения', required=False)
    text_content = serializers.CharField(label='Сообщение')

    def to_representation(self, instance):
        representation = super(MessageSerializer, self).to_representation(instance)
        representation['point'] = instance.point.__str__()
        return representation

    class Meta:
        model = Message
        fields = ['point', 'text_content', 'user', 'time_create']
