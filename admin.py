from django.contrib import admin  # type: ignore[reportMissingModuleSource]
from .models import Room, Student

admin.site.register(Room)
admin.site.register(Student)