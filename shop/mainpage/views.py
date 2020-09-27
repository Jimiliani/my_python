from django.core.mail import send_mail
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .models import Item
from .serializers import ItemSerializer, UnderwearSerializer, OutwearSerializer, ShoesSerializer, AccessoriesSerializer, \
    UnderwearMiniSerializer, OutwearMiniSerializer, ShoesMiniSerializer, AccessoriesMiniSerializer


def mainpage_view(request):
    return render(request, 'mainpage/mainpage.html')


def search_view(request):
    return render(request, 'search/search.html')


def detail_view(request, pk):
    item = Item.objects.get(id=pk)
    if item.item_type == 'Underwear':
        item = item.underwear
    elif item.item_type == 'Outwear':
        item = item.outwear
    elif item.item_type == 'Shoe':
        item = item.shoe
    elif item.item_type == 'Accessory':
        item = item.accessory
    return render(request, 'search/detail.html', {'item': item})


def bag_view(request):
    return render(request, 'profile/bag.html')


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List of items': 'item-list/',
        'Detail view of item': 'item-detail/<str:pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def get_item_list(request):
    items = Item.objects.all()
    gender = json.loads(request.query_params.get('gender', None))
    min_price = request.query_params.get('min_price', None)
    max_price = request.query_params.get('max_price', None)
    item_type = json.loads(request.query_params.get('item_type', None))
    if gender:
        items = items.filter(gender__in=gender)
    if min_price and max_price:
        items = items.filter(price__gte=float(min_price), price__lte=float(max_price))
    if item_type:
        items = items.filter(item_type__in=item_type)
    sort_type = request.query_params.get('sort_type', None)
    if sort_type == 'По возрастанию цены':
        items = items.order_by('price')
    elif sort_type == 'По убыванию цены':
        items = items.order_by('-price')
    elif sort_type == 'По наименованию товара':
        items = items.order_by('name')
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_item_detail(request, pk):
    item = Item.objects.get(id=pk)
    if item.item_type == 'Underwear':
        item = item.underwear
        serializer = UnderwearSerializer(item, many=False)
    elif item.item_type == 'Outwear':
        item = item.outwear
        serializer = OutwearSerializer(item, many=False)
    elif item.item_type == 'Shoe':
        item = item.shoe
        serializer = ShoesSerializer(item, many=False)
    elif item.item_type == 'Accessory':
        item = item.accessory
        serializer = AccessoriesSerializer(item, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_item_detail_slim(request, pk):
    item = Item.objects.get(id=pk)
    context = {'size': request.GET['size']}
    if item.item_type == 'Underwear':
        item = item.underwear
        serializer = UnderwearMiniSerializer(item, many=False, context=context)
    elif item.item_type == 'Outwear':
        item = item.outwear
        serializer = OutwearMiniSerializer(item, many=False, context=context)
    elif item.item_type == 'Shoe':
        item = item.shoe
        serializer = ShoesMiniSerializer(item, many=False, context=context)
    elif item.item_type == 'Accessory':
        item = item.accessory
        serializer = AccessoriesMiniSerializer(item, many=False, context=context)
    return Response(serializer.data)


@api_view(['POST'])
def pay(request):
    email = request.POST['email']
    items = json.loads(request.POST['items'])
    for item in items:
        selected_item = Item.objects.get(id=item['id'])
        if selected_item.item_type == 'Underwear':
            selected_item = selected_item.underwear
        elif selected_item.item_type == 'Outwear':
            selected_item = selected_item.outwear
        elif selected_item.item_type == 'Shoe':
            print('это обувь')
            selected_item = selected_item.shoe
        elif selected_item.item_type == 'Accessory':
            selected_item = selected_item.accessory
        if selected_item.buy_items(size=item['size'], count=int(item['count'])) is None:
            send_mail(
                'Ваши покупки',
                'К сожалению один из товаров закончился на складе, пожалуйста выберите товары и проведите оплату снова.',
                'dikorolyov2@gmail.ru',
                [email],
                fail_silently=False,
            )
            return redirect('mainpage:mainpage')
    send_mail(
        'Ваши покупки',
        'Покупка прошла успешно, спасибо, что пользуетесь нашим магазином!',
        'dikorolyov2@gmail.ru',
        [email],
        fail_silently=False,
    )
    return redirect('mainpage:mainpage')
