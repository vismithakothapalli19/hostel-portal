from django.db import models  # pyright: ignore[reportMissingModuleSource]

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=2)

    def __str__(self):
        return f"Room {self.room_number}"

class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"