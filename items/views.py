from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Collection, Item, ItemImageColor
from .serializers import CollectionGetSerializer, CollectionCreateSerializer, ItemsDetailSerializer,\
    ItemsListSerializer, ItemCreateSerializer

from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView


class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CollectionListView(ListAPIView):
    serializer_class = CollectionGetSerializer
    queryset = Collection.objects.all().order_by('-id')
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super(CollectionListView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class CollectionCreateView(CreateAPIView):
    serializer_class = CollectionCreateSerializer
    queryset = Collection.objects.all()

    def get_serializer_context(self):
        context = super(CollectionCreateView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class CollectionAPIView(APIView):
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
    serializer_class = ItemsListSerializer
    queryset = Item.objects.all().order_by('-id')
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super(ItemListView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class ItemCreateView(CreateAPIView):
    serializer_class = ItemCreateSerializer
    queryset = Item.objects.all()

    def get_serializer_context(self):
        context = super(ItemCreateView, self).get_serializer_context()
        context.update({"context": self.request})
        return context
