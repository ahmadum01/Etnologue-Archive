from django import views
from django.shortcuts import render
import langs.services as services


class MainPageView(views.View):
    def get(self, request):
        return render(request, 'langs/main_page.html')


class LangsView(views.View):
    def get(self, request, letter='a'):
        return render(request, 'langs/language_name.html', context={
            'pagination_letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZǀǂǁ',
            'languages': services.get_languages_by_letter(letter),
        })


class CodesView(views.View):
    def get(self, request, letter='a'):
        return render(request, 'langs/language_code.html', context={
            'iso_s': services.get_iso_by_letter(letter),
            'pagination_letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        })


class MapPointsView(views.View):
    def get(self, request, letter='a'):
        return render(request, 'langs/points.html', context={
            'map_points': services.get_map_points_by_letter(letter),
            'pagination_letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        })


class LangDetailView(views.View):
    def get(self, request, iso):
        return render(request, 'langs/lang_detail.html', context={
            'language': services.get_language_detail(iso),
            'point': services.get_map_point(iso),
        })


class SearchResultsView(views.View):
    def get(self, request):
        query = request.GET.get('q')
        return render(request, 'langs/search.html', context={
            'languages': services.get_search_result(query),
        })


