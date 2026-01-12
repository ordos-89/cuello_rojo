from django.contrib.gis.db import models
from users.models import Raider


class Point(models.Model):
    """Точка на карте"""
    title = models.CharField(max_length=255, blank=True, verbose_name="Название точки")
    location = models.PointField(verbose_name="Локация")
    user = models.ForeignKey(Raider, on_delete=models.SET_NULL, null=True,
                             verbose_name="отмечена Искателем")

    def __str__(self):
        return self.title if self.title else "unknown"


class Message(models.Model):
    """Сообщение к точке"""
    text_content = models.TextField(verbose_name="Текст сообщения", blank=False)
    point = models.ForeignKey(Point, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(Raider, on_delete=models.SET_NULL, null=True,
                             verbose_name="Сообщает Искатель", related_name="messages")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="временная метка")

    def __str__(self):
        timestamp = self.time_create.strftime('%d.%m.%Y %H:%M')
        return f"Место: {self.point}; оставил: {self.user} {timestamp}"
