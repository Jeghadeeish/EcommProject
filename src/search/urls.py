from django.contrib import admin
from django.urls import path,include

from search.views import SearchProductListView

app_name = 'products'
urlpatterns = [
    path('',SearchProductListView.as_view(), name='query'),
]

