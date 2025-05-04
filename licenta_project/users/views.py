from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from virtual_garden.models import VirtualGarden, GardenFlower
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
            
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }    
    return render(request, 'users/profile.html', context)

class UserProfileView(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        garden = VirtualGarden.objects.filter(user=user).first()
        context['garden_flowers'] = GardenFlower.objects.filter(garden=garden, unlocked=True) if garden else []
        
        return context