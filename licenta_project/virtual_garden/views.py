from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta

from .models import VirtualGarden, GardenFlower, Flower, GardenSlot
from django.contrib.auth.models import User
from blog.models import Activity  # Înlocuiește cu numele real al modelului tău

class VirtualGardenView(LoginRequiredMixin, TemplateView):
    template_name = 'virtual_garden/virtual_garden.html'
    context_object_name = 'virtual_garden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        garden, created = VirtualGarden.objects.get_or_create(user=self.request.user)
        context['garden'] = garden
        context['garden_flowers'] = GardenFlower.objects.filter(garden=garden).select_related('flower')
        
        # Add community data
        context['recent_activities'] = Activity.objects.select_related('user').order_by('-timestamp')[:10]
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Calculate unlocked count for current user
        unlocked_count = context['garden_flowers'].filter(unlocked=True).count()
        context['unlocked_count'] = unlocked_count
        
        return context

@login_required
def user_garden_view(request, username):
    user = get_object_or_404(User, username=username)
    garden, _ = VirtualGarden.objects.get_or_create(user=user)

    slots = []
    for i in range(18):
        slot, _ = GardenSlot.objects.get_or_create(garden=garden, slot_index=i)
        slots.append(slot)
        
    flowers = Flower.objects.all()
    planted_flower_ids = [slot.flower.id for slot in slots if slot.flower]

    garden_flowers_qs = GardenFlower.objects.filter(garden=garden).select_related('flower')
    
    garden_flowers = [
        {
            'flower': gf.flower,
            'unlocked': gf.unlocked and gf.flower.id not in planted_flower_ids
        }
        for gf in garden_flowers_qs
    ]

    if request.method == 'POST' and request.user == user:
        for slot in slots:
            flower_id = request.POST.get(f'flower_{slot.slot_index}')
            if flower_id:
                flower = Flower.objects.get(id=flower_id)
                slot.flower = flower
            else:
                slot.flower = None
            slot.save()
        return redirect('user-garden', username=username)

    return render(request, 'virtual_garden/user_garden.html', {
        'slots': slots,
        'flowers': flowers,
        'garden_owner': user,
        'garden_flowers': garden_flowers,
    })