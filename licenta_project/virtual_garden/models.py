from django.db import models
from django.contrib.auth.models import User

class Flower(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_path = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class VirtualGarden(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Garden"

class GardenFlower(models.Model):
    garden = models.ForeignKey(VirtualGarden, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)

    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)

    class Meta:
        unique_together = ('garden', 'flower')

    def __str__(self):
        return f"{self.flower.name} in {self.garden.user.username}'s garden"

class GardenSlot(models.Model):
    garden = models.ForeignKey(VirtualGarden, on_delete=models.CASCADE, related_name='slots')
    slot_index = models.PositiveIntegerField(default=0)
    flower = models.ForeignKey(Flower, null=True, blank=True, on_delete=models.SET_NULL)
    unlocked = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('garden','slot_index')

    