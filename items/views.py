import uuid

from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from .models import Collection, Item, ItemImageColor, ItemCart
from .serializers import CollectionGetSerializer, CollectionCreateSerializer, ItemsDetailSerializer, \
    ItemsListSerializer, ItemCreateSerializer, BasketSerializer, BasketListSerializer, BasketCreateSerializer

from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView


class CustomPagination(PageNumberPagination):
    '''class for pagination'''

    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CollectionListView(ListAPIView):
    '''view for  collections List'''

    serializer_class = CollectionGetSerializer
    queryset = Collection.objects.all().order_by('-id')
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super(CollectionListView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class CollectionCreateView(CreateAPIView):
    '''view for create new collection'''

    serializer_class = CollectionCreateSerializer
    queryset = Collection.objects.all()

    def get_serializer_context(self):
        context = super(CollectionCreateView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class CollectionAPIView(APIView):
    '''view for collection get by pk
        update collection and delete.
    '''

    queryset = Collection.objects.all()

    def get(self, request, pk):
        collection = get_object_or_404(self.queryset, pk=pk)
        serializer = CollectionGetSerializer(collection, context={'context': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        collection = get_object_or_404(self.queryset, pk=pk)
        serializer = CollectionCreateSerializer(collection, data=request.data,
                                    partial=True, context={'context': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        collection = get_object_or_404(self.queryset, pk=pk)
        serializer = CollectionCreateSerializer(collection, data=request.data,
                                    partial=True, context={'context': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collection = get_object_or_404(self.queryset, pk=pk)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemAPIView(APIView):
    '''view for get item by pk
        update item and delete
    '''

    queryset = Item.objects.all()

    def get(self, request, pk):
        collection = get_object_or_404(self.queryset, pk=pk)
        serializer = ItemsDetailSerializer(collection, context={'context': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        collection = get_object_or_404(self.queryset, pk=pk)
        serializer = ItemCreateSerializer(collection, data=request.data,
                                    partial=True, context={'context': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        collection = get_object_or_404(self.queryset, pk=pk)
        serializer = ItemCreateSerializer(collection, data=request.data,
                                    partial=True, context={'context': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collection = get_object_or_404(self.queryset, pk=pk)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemListView(ListAPIView):
    '''view for items list and filtering'''

    serializer_class = ItemsListSerializer
    queryset = Item.objects.all().order_by('-id')
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['collection', 'is_in_favourite', 'is_bestseller', 'is_novelty']
    search_fields = ['title']

    def get_serializer_context(self):
        context = super(ItemListView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class ItemCreateView(CreateAPIView):
    '''view for create new item'''

    serializer_class = ItemCreateSerializer
    queryset = Item.objects.all()

    def get_serializer_context(self):
        context = super(ItemCreateView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class APIBasketCreateView(CreateAPIView):
    '''create new basket'''

    serializer_class = BasketCreateSerializer
    queryset = ItemCart.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class APIBasketDeleteAllView(APIView):
    '''delete all basket'''

    def delete(self, request, *args, **kwargs):
        ItemCart.objects.all().delete()

        return Response(status=204)


class APIAddBasketView(APIView):
    '''view for show all items in basket and plus and minus quantity items in basket'''

    serializer_class = BasketSerializer
    model = ItemCart

    def get(self, request, *args, **kwargs):
        queryset = ItemCart.objects.all()
        serializer = BasketListSerializer(queryset, many=True, context={'context': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data['item']
        order = serializer.validated_data['order']
        if ItemCart.objects.filter(item=item, order=order).exists():
            orderitem = ItemCart.objects.filter(item=item, order=order).first()
            orderitem.amount += 1
            orderitem.save()
        else:
            orderitem = ItemCart.objects.create(
                item=item,
                amount=1,
                order=order
            )
            return Response({'amount': orderitem.amount}, status=201)
        return Response({'amount': orderitem.amount}, status=200)

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data['item']
        if ItemCart.objects.filter(item=item).exists():
            orderitem = ItemCart.objects.filter(item=item).first()
            orderitem.amount -= 1
            orderitem.save()
            if orderitem.amount < 1:
                orderitem.delete()
                return Response({'amount': orderitem.amount}, status=204)

        else:
            return Response({'amount': 0}, status=200)
        return Response({'amount': orderitem.amount}, status=200)


class APIBasketTotalPriceView(APIView):
    '''view for show total item price in basket'''

    def get(self, request, *args, **kwargs):
        total = ItemCart.get_total_price_of_item()
        return Response({"total_price": total}, status=200)


class APIBasketTotalQuantityView(APIView):
    '''view for show total item quantity in basket'''

    def get(self, request, *args, **kwargs):
        total = ItemCart.get_total_quantity_of_item()
        return Response({"total_quantity": total}, status=200)
