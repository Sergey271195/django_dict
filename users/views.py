from django.shortcuts import render
from django.views.generic import CreateView, TemplateView 
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import Profile



class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        print(request.user.id)
        profile = Profile.objects.filter(user_id = request.user.id)
        print(profile)
        return render(request, self.template_name, {'profile': profile})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context
