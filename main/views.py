from django.shortcuts import render
from django.views.generic import TemplateView 
from .websterapi import GetWordDefinition



class HomePageView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        word = request.GET.get('word')
        if word != None:
            result = GetWordDefinition(word).get_definition()
            if 'Error_links' in result:
                return(render(request, self.template_name, {'Error_links': result['Error_links']}))
            else:
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

