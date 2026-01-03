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

    def validate_left_by(self, value):
        """Мы должны найти Искателя по username или позывному (call_sign) и вернуть его объект для добавления
        ForeignKey к точке"""
        try:
            raider = Raider.objects.get(Q(username=value) | Q(call_sign=value))
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Неверно указан позывной или пользователь не зарегистрирован.")
        else:
            return raider

    class Meta:
        model = Point
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор модели Сообщения"""

    class Meta:
        model = Message
        fields = "__all__"