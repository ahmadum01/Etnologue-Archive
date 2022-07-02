from django import views
from django.http import HttpResponse
from .parse_services.languages import get_map_points, get_iso, Parser, get_langs
from langs.models import Iso, MapPoint, Language
import time


class FillIso(views.View):
    def get(self):
        all_iso = get_iso()
        for letter in all_iso:
            print(letter)
            for iso in all_iso[letter]:
                Iso.objects.create(iso=iso)
        return HttpResponse(b'Success')


class FillMapPoints(views.View):
    def get(self):
        all_map_points = get_map_points()
        counter = 0
        for map_point in all_map_points:
            print(counter)
            MapPoint.objects.create(
                iso=Iso.objects.get(iso=map_point['iso']),
                north=map_point['north'],
                south=map_point['south'],
                east=map_point['east'],
                west=map_point['west'],
            )
            counter += 1
        return HttpResponse(b'Success')


class FillLangDetail(views.View):
    def get(self, request):
        langs = get_langs()
        selected_letter = 'g'
        length = len(langs[selected_letter])
        count = 0
        start = time.perf_counter()
        flag = True
        for lang_name, link in langs[selected_letter]:
            count += 1
            # if flag:
            #     if link.split('/')[-1] == 'fom':
            #         flag = False
            #         continue
            #     else:
            #         continue
            print(f'{count} from {length}')

            lang_detail = Parser.parse_lang_detail(lang_name, link)
            Language.objects.create(
                language_name=lang_detail['language_name'],
                language_of=lang_detail['language_of'],
                iso=Iso.objects.get(iso=lang_detail['iso']),
                alternate_names=lang_detail['alternate_names'],
                autonym=lang_detail['autonym'],
                user_population=lang_detail['user_population'],
                location=lang_detail['location'],
                language_maps=lang_detail['language_maps'],
                language_status=lang_detail['language_status'],
                classification=lang_detail['classification'],
                dialects=lang_detail['dialects'],
                typology=lang_detail['typology'],
                language_use=lang_detail['language_use'],
                language_development=lang_detail['language_development'],
                language_resource=lang_detail['language_resource'],
                writing=lang_detail['writing'],
                other_comments=lang_detail['other_comments'],
            )
        finish = time.perf_counter()
        print(f'{finish - start} секунды')
        print(f'{int((finish - start) / 60)} минуты')
        print(f'{int((finish - start) // 60 // 60)} часа')
        return HttpResponse(b'Success')
