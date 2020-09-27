from django.urls import path
from mainpage.views import *

app_name = 'mainpage'

urlpatterns = [
    path('', mainpage_view, name='mainpage'),
    path('search/', search_view, name='search'),
    path('detail/<str:pk>', detail_view, name='item-detail'),
    path('bag/', bag_view, name='bag'),
    path('pay/', pay, name='pay'),
    path('api_overview/', api_overview, name='api-overview'),
    path('item_list/', get_item_list, name='api-item-list'),
    path('item_detail/<str:pk>', get_item_detail, name='api-item-detail'),
    path('item_detail_slim/<str:pk>', get_item_detail_slim, name='api-item-detail-slim'),
]
