from django.contrib.gis.db import models
from users.models import Raider


class Point(models.Model):
    """Точка на карте"""
    title = models.CharField(max_length=255, blank=True, verbose_name="Название точки")
    location = models.PointField(verbose_name="Координаты")
    left_by = models.ForeignKey(Raider, on_delete=models.SET_NULL, null=True,
                                verbose_name="оставлена Искателем")


class Message(models.Model):
    """Сообщение к точке"""
    text_content = models.TextField(verbose_name="Текст сообщения", blank=False)
    point = models.ForeignKey(Point, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(Raider, on_delete=models.SET_NULL, null=True,
                             verbose_name="Сообщает Искатель", related_name="messages")
