from random import choice
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView

from .models import Collection, Item, ItemCart, Order, OrderItem, UserFavouriteItems
from .serializers import CollectionGetSerializer, ItemsDetailSerializer, \
    ItemsListSerializer, BasketSerializer, BasketListSerializer, \
    BasketCreateSerializer, OrderSerializer, OrderListSerializer, OrderDetailSerializer, \
    UserFavouriteItemSerializer, UserFavouriteCreateSerializer


class CustomPagination(PageNumberPagination):
    """class for pagination"""

    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CollectionListView(ListAPIView):
    """view for collections List"""

    serializer_class = CollectionGetSerializer
    queryset = Collection.objects.all().order_by('-id')
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super(CollectionListView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class CollectionAPIView(APIView):
    """view for collection get by pk  """

    queryset = Collection.objects.all()

    def get(self, request, pk):
        collection = get_object_or_404(self.queryset, pk=pk)
        serializer = CollectionGetSerializer(collection, context={'context': request})
        return Response(serializer.data)


class ItemAPIView(RetrieveAPIView):
    """view for get item by pk """

    queryset = Item.objects.all()
    serializer_class = ItemsDetailSerializer

    def get_serializer_context(self):
        context = super(ItemAPIView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class ItemListView(ListAPIView):
    """view for items list and filtering"""

    serializer_class = ItemsListSerializer
    queryset = Item.objects.all().order_by('-id')
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['collection', 'is_bestseller', 'is_novelty',]
    search_fields = ['title', 'collection__name']

    def get_serializer_context(self):
        context = super(ItemListView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class SameItemListView(ListAPIView):
    """return same 5 item by collection """

    serializer_class = ItemsListSerializer

    def get_serializer_context(self):
        context = super(SameItemListView, self).get_serializer_context()
        context.update({"context": self.request})
        return context

    def get_queryset(self):
        queryset = Item.objects.all()
        collection = self.request.query_params.get('collection_id')
        if collection is not None:
            queryset = queryset.filter(collection__id=collection).order_by('?')[:5]
        return queryset


class NoveltyItemView(ListAPIView):
    """return 4 novelty item for main page"""
    serializer_class = ItemsListSerializer

    def get_serializer_context(self):
        context = super(NoveltyItemView, self).get_serializer_context()
        context.update({"context": self.request})
        return context

    def get_queryset(self):
        queryset = Item.objects.all()
        novelty = self.request.query_params.get('is_novelty')
        if novelty is not None:
            queryset = queryset.filter(is_novelty=novelty).order_by('-id')[:4]
        return queryset


class APIBasketCreateView(CreateAPIView):
    """create new basket"""

    serializer_class = BasketCreateSerializer
    queryset = ItemCart.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'context': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class APIBasketDeleteAllView(APIView):
    """delete all basket"""
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        ItemCart.objects.all().delete()

        return Response(status=204)


class DeleteOneAmountBasketView(APIView):
    """method for delete amount in basket by one"""
    serializer_class = BasketSerializer
    model = ItemCart

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'context': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data['item']
        image = serializer.validated_data['image']
        if ItemCart.objects.filter(item=item, image=image).exists():
            orderitem = ItemCart.objects.filter(item=item, image=image).first()
            orderitem.amount -= 1
            orderitem.save()
            if orderitem.amount <= 1:
                orderitem.delete()
                return Response({'amount': orderitem.amount}, status=204)

        else:
            return Response({'amount': 0}, status=200)
        return Response({'amount': orderitem.amount}, status=200)


class DeleteByPKBasketView(APIView):
    """delete one object from basket"""

    def get_object(self, pk):
        try:
            return ItemCart.objects.get(pk=pk)
        except ItemCart.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        basket = self.get_object(pk)
        basket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIAddBasketView(APIView):
    """view for show all items in basket add amount item by one in basket"""

    serializer_class = BasketSerializer
    model = ItemCart

    """method for list all item in the basket"""

    def get(self, request, *args, **kwargs):
        queryset = ItemCart.objects.all()
        serializer = BasketListSerializer(queryset, many=True, context={"context": request})
        return Response(serializer.data)

    """method for add amount in basket by 1"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'context': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data['item']
        image = serializer.validated_data['image']
        if ItemCart.objects.filter(item=item, image=image).exists():
            orderitem = ItemCart.objects.filter(item=item, image=image).first()
            orderitem.amount += 1
            orderitem.save()

        else:
            orderitem = ItemCart.objects.create(
                item=item,
                image=image,
                amount=1,
            )
            return Response({'amount': orderitem.amount}, status=201)
        return Response({'amount': orderitem.amount}, status=200)


class APIBasketTotalPriceView(APIView):
    """view for show total item price before and after discount in basket,
        sum of discount, total item quantity and total item quantity line in basket
    """

    def get(self, request, *args, **kwargs):
        total_before = ItemCart.get_total_price_of_item_before_discount()
        total_after = ItemCart.get_total_price_of_item_after_discount()
        discount = total_before - total_after
        total_quantity = ItemCart.get_total_quantity_of_item()
        amount = ItemCart.get_total_quantity_of_item_line()

        return Response({"Сумма товаров до скидки": total_before,
                         'итоговая цена': total_after,
                         'сумма скидки': discount,
                         'количество товаров в корзине': total_quantity,
                         'количество линеек в корзине': amount
                         }, status=200)


class OrderCreateView(CreateAPIView):
    """create order and save it in order item,
        after saved delete all item in the basket, and update order status to framed"""

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        order = serializer.save()

        for i in ItemCart.objects.all():
            OrderItem.objects.create(item=i.item, title=i.item.title, image=i.image, order=order)

        self.queryset.update(order_status="FRAMED")
        ItemCart.objects.all().delete()


class ItemRandomView(APIView):
    """view for return random 5 item list"""

    serializer_class = ItemsListSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            collection = list(Collection.objects.values_list('id', flat=True).order_by('?'))
            queryset = list(choice(self.queryset.filter(collection__id=pk).order_by('?')) for pk in collection)[:5]
            serializer = self.serializer_class(queryset, many=True, context={'context': request})
            return Response(serializer.data)
        except IndexError:
            queryset = self.queryset.order_by('?')[:5]
            serializer = self.serializer_class(queryset, many=True, context={'context': request})
            return Response(serializer.data)


class OrderListView(ListAPIView):
    """view for get list order"""
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()


class OrderDetailView(RetrieveAPIView):
    """view for get order detail"""

    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

    def get_serializer_context(self):
        context = super(OrderDetailView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class UserFavouriteList(ListAPIView):
    serializer_class = UserFavouriteItemSerializer
    queryset = UserFavouriteItems.objects.order_by('-id')

    def get_queryset(self):
        user = self.request.user
        return UserFavouriteItems.objects.filter(user=user)

    def get_serializer_context(self):
        context = super(UserFavouriteList, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class UserFavouriteCreate(CreateAPIView):
    serializer_class = UserFavouriteCreateSerializer
    queryset = UserFavouriteItems.objects.all()

    def get_queryset(self):
        user = self.request.user
        return UserFavouriteItems.objects.filter(user=user)

    def get_serializer_context(self):
        context = super(UserFavouriteCreate, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class ItemFavoriteDestroyByItemView(APIView):
    queryset = UserFavouriteItems.objects.all()

    def post(self, request):
        item = UserFavouriteItems.objects.get(item__id=request.data.get('item_id'))
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


