from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Point, Message


@admin.register(Point)
class PointAdmin(GISModelAdmin):
    list_display = ('title', 'location', 'user')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text_content', 'point', 'user', 'time_create')
