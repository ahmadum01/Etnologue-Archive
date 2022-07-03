import parsing.services as services
from django import views
from django.http import HttpResponse
from .parse_services.languages import get_map_points, get_iso, Parser, get_langs


class FillIso(views.View):
    def get(self):
        all_iso = get_iso()
        for letter in all_iso:
            print(letter)
            for iso in all_iso[letter]:
                services.create_iso(iso)
        return HttpResponse(b'Success')


class FillMapPoints(views.View):
    def get(self):
        all_map_points = get_map_points()
        counter = 0
        for map_point in all_map_points:
            counter += 1
            print(counter)
            services.create_map_point(map_point)
        return HttpResponse(b'Success')


class FillLangDetail(views.View):
    def get(self, request):
        print(services.get_langs_count())
        langs = get_langs()
        selected_letter = 'ǁ'.lower()
        length = len(langs[selected_letter])
        counter = 0
        for lang_name, link in langs[selected_letter]:
            counter += 1
            print(f'{counter} from {length}')
            lang_detail = Parser.parse_lang_detail(lang_name, link)
            services.create_language(lang_detail)

        return HttpResponse(b'Success')
