from django.shortcuts import render
from django.views.generic import TemplateView 
from .websterapi import GetWordDefinition
from users.models import Word
import django.dispatch
from django.db import IntegrityError

valid_request_to_history = django.dispatch.Signal(providing_args=["user_id", "word_id"])
valid_request_to_local_history = django.dispatch.Signal(providing_args=["user_id", "word_id"])

class HomePageView(TemplateView):
    template_name = 'home.html'

    def request_to_history(self, user, word):
        print('REQUEST TO HISTORY', user.id, word.id)
        valid_request_to_history.send(sender = self.__class__, user_id = user.id, word_id = word.id)

    def get(self, request, *args, **kwargs):
        word = request.GET.get('word')
        if word != None:
            result = GetWordDefinition(word).get_definition()
            if 'Error_links' in result:
                return(render(request, self.template_name, {'Error_links': result['Error_links'], 'search': word.capitalize()}))
            else:

                ### Saving new word to database

                try:
                    word_to_db = Word.objects.create(word = word.lower())
                    word_to_db.save()
                    print(f'Saved {word_to_db}')
                except IntegrityError as e:
                    print(f'Word "{word}" already exisits in db')

                
                ### Saving word to search history
                
                word_to_history = Word.objects.get(word = word)
                self.request_to_history(request.user, word_to_history)


                definition = result[0]
                if len(result) > 1:
                    general_info = result[1]
                else:
                    general_info = None
                return(render(request, self.template_name, {'definition': definition, 'general_info': general_info, 'search': word.capitalize()}))
        else:
            return(render(request, self.template_name))

    """ def post(self, request, *args, **kwargs):
        print('Post')
        print(request.POST.get('word'))
        word = request.POST.get('word')
        result = GetWordDefinition(word).get_definition()
        definition = result[0]
        if len(result) > 1:
            general_info = result[1]
        else:
            general_info = None
        return(render(request, self.template_name, {'definition': definition, 'general_info': general_info, 'search': word.capitalize()})) """

