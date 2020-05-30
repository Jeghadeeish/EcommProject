from django.contrib import admin
from django.urls import path,include

from products.views import ProductListView, ProductSlugDetailView

app_name = 'products'
urlpatterns = [
    path('',ProductListView.as_view(), name='list'),
    path('<slug:slug>/',ProductSlugDetailView.as_view(),name='detail')
]

