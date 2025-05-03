from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import VirtualGarden, Flower, GardenFlower

@receiver(post_save, sender=User)
def create_virtual_garden(sender, instance, created, **kwargs):
    if created:
        garden = VirtualGarden.objects.create(user=instance)
        
        flowers = list(Flower.objects.all())
        garden_flowers = []
        
        for flower in flowers:
            garden_flowers.append(GardenFlower(
                garden=garden,
                flower=flower,
                unlocked=False
            ))
        
        if garden_flowers:
            GardenFlower.objects.bulk_create(garden_flowers)
