# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('buscar_review', views.buscar_review, name='buscar_review'),
    path('baixar_excel', views.baixar_excel, name='baixar_excel'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    

]
