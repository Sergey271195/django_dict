from django.shortcuts import render
from django.views.generic import CreateView, TemplateView 
from django.urls import reverse_lazy
from django.http import JsonResponse

import random


from .forms import CustomUserCreationForm
from .models import Profile, CustomUser
from .models import Word
from main.websterapi import GetWordDefinition




class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_random_words(self, request):
        words = self.get_context(request)
        words = [value['word'] for value in list(words.values('word'))]
        try:
            random_words = random.sample(words, 10)
        except Exception as e:
            random_words = random.sample(words, len(words))
        short_definitions = {}
        for word in random_words:
            shortdef = GetWordDefinition(word).profile_search()
            short_definitions[word] = shortdef
        return short_definitions


    def handle_ajax(self, request):
        if 'start' in request.GET:
            response = self.get_random_words(request)
            return response
        elif 'filter' in request.GET:
            filt = request.GET.get('filter')
            words = self.get_context(request)
            if filt != '':
                words = words.filter(word__startswith = filt.lower()).order_by('word')
            response = [w.word for w in words]
            return response
        elif 'delete' in request.GET:
            delete_request = request.GET.get('delete')
            delete_word = Word.objects.get(word = delete_request.lower())
            Profile.objects.get(user_id = request.user.id, history_id = delete_word.id).delete()
            try:
                Profile.objects.get(user_id = request.user.id, local_history_id = delete_word.id).delete()
            except Exception as e:
                pass

    def get_context(self, request):
        profile = Profile.objects.filter(user_id = request.user.id).exclude(history_id = None).values('history_id')
        result = [values['history_id'] for values in list(profile)]
        words = Word.objects.filter(id__in= result).order_by('word')
        return words

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            response = self.handle_ajax(request)
            data = {
                'words': response,
            }
            return JsonResponse(data, safe = False)
        words = self.get_context(request)
        return render(request, self.template_name, {'profile': words, 'added': request.user.add_all})

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id = request.user.id)
        if 'add_chosen' in request.POST:
            user.add_all = False
            user.save(update_fields=["add_all"])
        elif 'add_all' in request.POST:
            user.add_all = True
            user.save(update_fields=["add_all"])
        words = self.get_context(request)
        return render(request, self.template_name, {'profile': words, 'added': user.add_all})


