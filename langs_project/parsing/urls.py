from django.contrib import admin
from django.urls import path, include
from .views import FillMapPoints, FillIso, FillLangDetail

urlpatterns = [
    path('fill_iso/', FillIso.as_view()),
    path('fill_map/', FillMapPoints.as_view()),
    path('fill_lang_detail/', FillLangDetail.as_view()),
]

