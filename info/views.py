from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import AboutUs, News, Help, Offer, Contacts, MainPageIcon, Advantages, CallBack
from .serializers import AboutSerializer, NewsSerializer, HelpSerializer, OfferSerializer,\
    ContactsSerializer, MainPageIconSerializer, AdvantagesSerializer, CallBackSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class CallBackViewSet(viewsets.ModelViewSet):
    queryset = CallBack.objects.all()
    serializer_class = CallBackSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class MainPageViewSet(viewsets.ModelViewSet):
    queryset = MainPageIcon.objects.all()
    serializer_class = MainPageIconSerializer


class AdvantagesViewSet(viewsets.ModelViewSet):
    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-id')
    serializer_class = OfferSerializer


class HelpViewSet(viewsets.ModelViewSet):
    queryset = Help.objects.all().order_by('-id')
    serializer_class = HelpSerializer

