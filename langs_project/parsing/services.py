from langs.models import Language, Iso, MapPoint


def create_iso(iso: str) -> None:
    Iso.objects.create(iso=iso)


def create_language(lang_detail: dict) -> None:
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


def create_map_point(map_point: dict) -> None:
    MapPoint.objects.create(
        iso=Iso.objects.get(iso=map_point['iso']),
        north=map_point['north'],
        south=map_point['south'],
        east=map_point['east'],
        west=map_point['west'],
    )


def get_langs_count() -> int:
    return Language.objects.count()
