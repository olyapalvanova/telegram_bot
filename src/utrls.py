from django.urls import re_path, include


urlpatterns = [
    re_path('', include(('src.software.utrls', 'software'), namespace='software')),
]
