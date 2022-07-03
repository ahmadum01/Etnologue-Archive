from .models import Language, Iso, MapPoint
from django.db.models import Q, QuerySet


def get_languages_by_letter(letter) -> QuerySet:
    match letter:
        case 'a':
            return Language.objects.only('language_name', 'iso').filter(
                Q(language_name__istartswith=letter) | Q(language_name__istartswith='À') |
                Q(language_name__istartswith='Ä') | Q(language_name__istartswith='’A') |
                Q(language_name__istartswith='Á')
            )
        case 'n':
            return Language.objects.only('language_name', 'iso').filter(
                Q(language_name__istartswith=letter) | Q(language_name__istartswith='Ñ')
            )
        case 'o':
            return Language.objects.only('language_name', 'iso').filter(
                Q(language_name__istartswith=letter) | Q(language_name__istartswith='Ö')
            )
        case  'u':
            return Language.objects.only('language_name', 'iso').filter(
                Q(language_name__istartswith=letter) | Q(language_name__istartswith='‡U')
            )
        case 'x':
            return Language.objects.only('language_name', 'iso').filter(
                Q(language_name__istartswith=letter) | Q(language_name__istartswith='!X')
            )
        case _:
            return Language.objects.only('language_name', 'iso').filter(language_name__istartswith=letter)


def get_iso_by_letter(letter: str) -> QuerySet:
    return Iso.objects.filter(iso__istartswith=letter)


def get_map_points_by_letter(letter: str) -> QuerySet:
    return MapPoint.objects.order_by('iso').filter(iso__iso__istartswith=letter)


def get_language_detail(iso: str) -> Language:
    return Language.objects.get(iso__iso=iso)


def get_map_point(iso: str) -> MapPoint:
    return MapPoint.objects.get(iso__iso=iso)


def get_search_result(query: str, count=100) -> list:
    all_results = Language.objects.filter(
        Q(language_name__icontains=query) | Q(language_of__icontains=query)
    )
    result_starts_with = all_results.filter(language_name__istartswith=query)
    all_results = all_results.exclude(pk__in=result_starts_with)
    results_by_names = all_results.filter(language_name__icontains=query)
    all_results = all_results.exclude(pk__in=results_by_names)
    return (list(result_starts_with) + list(results_by_names) + list(all_results))[:count]