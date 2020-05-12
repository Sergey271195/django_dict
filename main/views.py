import json
from django.shortcuts import render
from django.views.generic import TemplateView 
import django.dispatch
from django.db import IntegrityError
from django.http import JsonResponse


from .websterapi import GetWordDefinition
from users.models import Word, Profile

class HomePageView(TemplateView):
    template_name = 'home.html'

    def request_to_history(self, user, word):
        check = Profile.objects.filter(user_id = user.id, history_id = word.id).exists()
        if not check:
            profile = Profile.objects.create(user_id = user.id, history_id = word.id)
            profile.save()

    
    def request_to_local_history(self, user, word):
        self.request_to_history(user, word)
        check = Profile.objects.filter(user_id = user.id, local_history_id = word.id).exists()
        if not check:
            profile = Profile.objects.create(user_id = user.id, local_history_id = word.id)
            profile.save()
            return True

    def handle_ajax_request(self, request):
        profile = Profile.objects.filter(user_id = request.user.id).exclude(local_history = None)
        word_list = []
        for entry in profile:
            word_list.append(str(entry.local_history))
        list_data_json = (list(word_list))
        
        data = {
            'words': list(word_list),
            }
        return JsonResponse(data, safe = False)


    def profile_check(self, request, word):
        word_check = Word.objects.get(word = word.lower())
        check = Profile.objects.filter(user_id = request.user.id, local_history_id = word_check.id).exists()
        return True if check else False


        

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'to_local_history' in request.GET:
                word = request.GET.get('to_local_history')
                word_to_local_history = Word.objects.get(word = word.lower())
                if self.request_to_local_history(request.user, word_to_local_history):
                    data = {'word': word.lower()}
                    return JsonResponse(data, safe = False)
            elif 'delete' in request.GET:
                delete_request = request.GET.get('delete')
                delete_word = Word.objects.get(word = delete_request.lower())
                Profile.objects.get(user_id = request.user.id, history_id = delete_word.id).delete()
            else:
                return self.handle_ajax_request(request)
        if 'to_local_history' in request.GET:
            word = request.GET.get('to_local_history')
        else:
            word = request.GET.get('word')
        if word != None and word != '':
            result = GetWordDefinition(word).get_definition()
            if 'Error_links' in result:
                return(render(request, self.template_name, {'Error_links': result['Error_links'], 'search': word.capitalize()}))
            else:

                ### Saving new word to database

                try:
                    word_to_db = Word.objects.create(word = word.lower())
                    word_to_db.save()
                except IntegrityError as e:
                    print(f'Word "{word}" already exisits in db')

                
                ### Saving word to search history
                
                if request.user.add_all:
                    word_to_history = Word.objects.get(word = word.lower())
                    self.request_to_history(request.user, word_to_history)

                ### Check if already added

                added = self.profile_check(request, word)

                definition = result[0]
                if len(result) > 1:
                    general_info = result[1]
                else:
                    general_info = None
                return(render(request, self.template_name, {'definition': definition, 'general_info': general_info, 'search': word.capitalize(), 'added': added}))
        else:
            return(render(request, self.template_name))


