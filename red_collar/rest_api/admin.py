from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Point, Message


admin.site.register(Message)


@admin.register(Point)
class PointAdmin(GISModelAdmin):
    list_display = ('title', 'location')
