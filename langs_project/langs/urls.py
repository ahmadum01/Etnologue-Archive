from django.urls import path
from .views import MainPageView, LangsView, LangDetailView, CodesView, MapPointsView, SearchResultsView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('browse/names/', LangsView.as_view(), name='lang_names'),
    path('browse/names/<str:letter>', LangsView.as_view(), name='lang_names_letter'),
    path('browse/codes/', CodesView.as_view(), name='lang_codes'),
    path('browse/codes/<str:letter>', CodesView.as_view(), name='lang_codes_letter'),
    path('browse/map-points/', MapPointsView.as_view(), name='map_points'),
    path('browse/map-points/<str:letter>', MapPointsView.as_view(), name='map_points_letter'),
    path('language/<str:iso>/', LangDetailView.as_view(), name='map_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
