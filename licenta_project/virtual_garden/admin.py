from django.contrib import admin
from .models import (Flower,
                     VirtualGarden,
                     GardenFlower,
                     GardenSlot)
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(VirtualGarden)
admin.site.register(GardenFlower)
admin.site.register(GardenSlot)

class FlowerAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'truncated_description')
    search_fields = ('name', 'description')
    
    def truncated_description(self, obj):
        if obj.description and len(obj.description) > 50:
            return obj.description[:50] + "..."
        return obj.description
    truncated_description.short_description = 'Description'

admin.site.register(Flower, FlowerAdmin)