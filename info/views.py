from django.shortcuts import render
from rest_framework.response import Response

from .models import AboutUs, News, Help, Offer
from .serializers import AboutSerializer, NewsSerializer, HelpSerializer, OfferSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class AboutUsView(APIView):

    def get(self, request, format=None):
        about = AboutUs.objects.all()
        serializer = AboutSerializer(about, many=True)
        return Response(serializer.data)


class NewsListView(APIView):

    def get(self, request):
        news = News.objects.all().order_by('-id')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


class NewsDetailView(APIView):

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)


class OfferListView(APIView):

    def get(self, request):
        offer = Offer.objects.all()
        serializer = OfferSerializer(offer, many=True)
        return Response(serializer.data)


class HelpListView(APIView):

    def get(self, request):
        help = Help.objects.all().order_by('-id')
        serializer = NewsSerializer(help, many=True)
        return Response(serializer.data)


class HelpDetailView(APIView):

    def get(self, request, pk):
        help = get_object_or_404(Help, pk=pk)
        serializer = NewsSerializer(help)
        return Response(serializer.data)