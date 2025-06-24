from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

from .models import VirtualGarden, GardenFlower, Flower, GardenSlot
from django.contrib.auth.models import User
from blog.models import Activity

class VirtualGardenView(LoginRequiredMixin, TemplateView):
    template_name = 'virtual_garden/virtual_garden.html'
    context_object_name = 'virtual_garden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        garden, created = VirtualGarden.objects.get_or_create(user=self.request.user)
        context['garden'] = garden
        context['garden_flowers'] = GardenFlower.objects.filter(garden=garden).select_related('flower')
                
        context['recent_activities'] = Activity.objects.select_related('user').order_by('-timestamp')[:10]
        context['total_users'] = User.objects.count()
        context['active_users'] = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=7)
        ).count()
                
        unlocked_count = context['garden_flowers'].filter(unlocked=True).count()
        context['unlocked_count'] = unlocked_count
                
        return context

def validate_flower_position_percentage(pos_x, pos_y):
    
    MIN_PERCENT = 5.0
    MAX_PERCENT = 95.0
    
    pos_x_valid = max(MIN_PERCENT, min(float(pos_x), MAX_PERCENT))
    pos_y_valid = max(MIN_PERCENT, min(float(pos_y), MAX_PERCENT))
    
    return round(pos_x_valid, 2), round(pos_y_valid, 2)

def convert_pixels_to_percentage(pixel_pos, is_x_axis=True):

    REFERENCE_WIDTH = 800
    REFERENCE_HEIGHT = 600
    FLOWER_SIZE = 80
    
    if is_x_axis:
        max_pos = REFERENCE_WIDTH - FLOWER_SIZE
        percentage = (pixel_pos / max_pos) * 100 if max_pos > 0 else 50
    else:
        max_pos = REFERENCE_HEIGHT - FLOWER_SIZE
        percentage = (pixel_pos / max_pos) * 100 if max_pos > 0 else 50
    
    return max(5, min(percentage, 95))

@login_required  
def user_garden_view(request, username):
    user = get_object_or_404(User, username=username)
    garden, _ = VirtualGarden.objects.get_or_create(user=user)

    slots = []
    for i in range(13):
        slot, _ = GardenSlot.objects.get_or_create(garden=garden, slot_index=i)
        slots.append(slot)
            
    flowers = Flower.objects.all()
    planted_flower_ids = [slot.flower.id for slot in slots if slot.flower]

    garden_flowers_qs = GardenFlower.objects.filter(garden=garden).select_related('flower')
        
    garden_flowers = [
        {
            'flower': gf.flower,
            'unlocked': gf.unlocked,
            'available_for_planting': gf.unlocked and gf.flower.id not in planted_flower_ids
        }
        for gf in garden_flowers_qs
    ]

    if request.method == 'POST' and request.user == user:
        validation_errors = []
        corrected_positions = 0
        migrated_positions = 0
        
        for slot in slots:
            flower_id = request.POST.get(f'flower_{slot.slot_index}')
            pos_x_str = request.POST.get(f'pos_x_{slot.slot_index}')
            pos_y_str = request.POST.get(f'pos_y_{slot.slot_index}')
                        
            if flower_id:
                try:
                    flower = Flower.objects.get(id=flower_id)
                    
                    garden_flower = GardenFlower.objects.filter(
                        garden=garden, 
                        flower=flower, 
                        unlocked=True
                    ).first()
                    
                    if not garden_flower:
                        validation_errors.append(f"Flower '{flower.name}' is locked")
                        continue
                    
                    slot.flower = flower
                                        
                    if pos_x_str and pos_y_str:
                        try:
                            pos_x_original = float(pos_x_str)
                            pos_y_original = float(pos_y_str)
                            
                            if pos_x_original > 100 or pos_y_original > 100:
                                pos_x_percent = convert_pixels_to_percentage(pos_x_original, True)
                                pos_y_percent = convert_pixels_to_percentage(pos_y_original, False)
                                migrated_positions += 1
                                
                                pos_x_valid, pos_y_valid = validate_flower_position_percentage(
                                    pos_x_percent, pos_y_percent
                                )
                                
                                print(f"Migrated flower '{flower.name}': "
                                      f"({pos_x_original}px, {pos_y_original}px) -> "
                                      f"({pos_x_valid}%, {pos_y_valid}%)")
                                
                            else:
                                pos_x_valid, pos_y_valid = validate_flower_position_percentage(
                                    pos_x_original, pos_y_original
                                )
                                
                                if abs(pos_x_original - pos_x_valid) > 0.01 or abs(pos_y_original - pos_y_valid) > 0.01:
                                    corrected_positions += 1
                                    validation_errors.append(
                                        f"Pos '{flower.name}': its ok now "
                                        f"from ({pos_x_original:.2f}%, {pos_y_original:.2f}%) "
                                        f"to ({pos_x_valid}%, {pos_y_valid}%) (extreme values)"
                                    )
                            
                            slot.pos_x = pos_x_valid
                            slot.pos_y = pos_y_valid
                            
                        except (ValueError, TypeError) as e:
                            print(f"Error processing pos for {flower.name}: {e}")
                            slot.pos_x = 5.0
                            slot.pos_y = 5.0
                            validation_errors.append(
                                f"Invalid pos for '{flower.name}'. "
                                f"Flower placed in the corner"
                            )
                    else:
                        slot.pos_x = 5.0
                        slot.pos_y = 5.0
                                        
                except Flower.DoesNotExist:
                    validation_errors.append(f"Flower with ID {flower_id} doesnt exist")
                    slot.flower = None
                    slot.pos_x = None
                    slot.pos_y = None
            else:
                slot.flower = None
                slot.pos_x = None
                slot.pos_y = None
                            
            slot.save()
        
        if migrated_positions > 0:
            messages.info(
                request, 
                f"Saved Garden, {migrated_positions} positions have been migrated"
            )
        elif validation_errors:
            if corrected_positions > 0:
                messages.warning(
                    request, 
                    f"Saved Garden, {corrected_positions} extreme positions have been corrected"
                )
            else:
                messages.success(request, "Successfully saved the garden")
        else:
            messages.success(request, "Successfully saved the garden")
                    
        return redirect('user-garden', username=username)

    return render(request, 'virtual_garden/user_garden.html', {
        'slots': slots,
        'flowers': flowers,
        'garden_owner': user,
        'garden_flowers': garden_flowers,
    })