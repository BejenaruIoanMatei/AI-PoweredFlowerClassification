from django.contrib import admin
from .models import (Flower,
                     VirtualGarden,
                     GardenFlower,
                     GardenSlot)

admin.site.register(Flower)
admin.site.register(VirtualGarden)
admin.site.register(GardenFlower)
admin.site.register(GardenSlot)