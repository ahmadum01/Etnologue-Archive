from django import views
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from .models import Iso, Language, MapPoint


class MainPageView(views.View):
    def get(self, request):
        return render(request, 'langs/main_page.html')


class LangsView(views.View):
    def get(self, request, letter='a'):
        context = {
            'languages': Language.objects.only('language_name', 'iso').filter(language_name__istartswith=letter),
            'pagination_letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZǀǂǁ',
        }
        return render(request, 'langs/language_name.html', context=context)


class CodesView(views.View):
    def get(self, request, letter='a'):
        context = {
            'iso_s': Iso.objects.filter(iso__istartswith=letter),
            'pagination_letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        }
        return render(request, 'langs/language_code.html', context=context)


class MapPointsView(views.View):
    def get(self, request, letter='a'):
        context = {
            'map_points': MapPoint.objects.order_by('iso').filter(iso__iso__istartswith=letter),
            'pagination_letters': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        }
        return render(request, 'langs/points.html', context=context)


class LangDetailView(views.View):
    def get(self, request, iso):
        context = {
            'language': Language.objects.get(iso__iso=iso),
            'point': MapPoint.objects.get(iso__iso=iso),
        }
        return render(request, 'langs/lang_detail.html', context=context)


class SearchResultsView(views.View):
    def get(self, request):
        query = request.GET.get('q')
        context = {
            'languages': Language.objects.filter(
                Q(language_name__icontains=query) | Q(language_of__icontains=query)
            )[:50]
        }
        return render(request, 'langs/search.html', context=context)


