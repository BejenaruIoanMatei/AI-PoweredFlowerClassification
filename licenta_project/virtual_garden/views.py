from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VirtualGarden, GardenFlower

class VirtualGardenView(LoginRequiredMixin, TemplateView):
    template_name = 'virtual_garden/virtual_garden.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Creează grădina dacă nu există deja
        garden, created = VirtualGarden.objects.get_or_create(user=self.request.user)

        # Adaugă grădina și florile din grădină în context
        context['garden'] = garden
        context['garden_flowers'] = GardenFlower.objects.filter(garden=garden).select_related('flower')
        return context