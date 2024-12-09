from django.urls import re_path

from src.software.views import (
    start, SoftwareViewSet, LicenseViewSet, show_statistics, TopForYearViewSet, TopForWeekViewSet, TopForMonthViewSet,
    OrderViewSet, OrderSumViewSet,
)

urlpatterns = [
    re_path('start', start, name='start'),
    re_path('main_menu', start, name='start'),

    re_path('show_statistics', show_statistics, name='show_statistics'),
    re_path('sf/', SoftwareViewSet, name='SoftwareViewSet'),
    re_path('lc/', LicenseViewSet, name='LicenseViewSet'),
    re_path('ord/', OrderViewSet, name='OrderViewSet'),
    re_path('tfy/', TopForYearViewSet, name='TopForYearViewSet'),
    re_path('tfm/', TopForMonthViewSet, name='TopForMonthViewSet'),
    re_path('tfw/', TopForWeekViewSet, name='TopForWeekViewSet'),
    re_path('ord_sum/', OrderSumViewSet, name='OrderSumViewSet'),
]
