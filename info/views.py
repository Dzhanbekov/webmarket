from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import AboutUs, News, Help, Offer, Contacts, MainPageIcon, Advantages, CallBack, HelpIcon
from .serializers import AboutSerializer, NewsSerializer, HelpSerializer, OfferSerializer, \
    ContactsSerializer, MainPageIconSerializer, AdvantagesSerializer, CallBackSerializer, HelpIconSerializer
from rest_framework import generics


class CustomPagination(PageNumberPagination):
    '''class for pagination'''

    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CallBackView(generics.CreateAPIView):
    """function for callback's all http methods"""

    queryset = CallBack.objects.all()
    serializer_class = CallBackSerializer


class ContactView(generics.ListAPIView):
    """function for contact's all http methods"""

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class MainPageView(generics.ListAPIView):
    """function for main pages all http methods"""

    queryset = MainPageIcon.objects.all()
    serializer_class = MainPageIconSerializer


class AdvantagesView(generics.ListAPIView):
    """function for advantages all http methods"""

    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer


class AboutUsView(generics.ListAPIView):
    """function for about uses all http methods"""

    queryset = AboutUs.objects.all()
    serializer_class = AboutSerializer


class NewsView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    pagination_class = CustomPagination


class NewsViewDetail(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class OfferView(generics.ListAPIView):
    queryset = Offer.objects.all().order_by('-id')
    serializer_class = OfferSerializer


class HelpView(generics.ListAPIView):
    queryset = Help.objects.all().order_by('-id')
    serializer_class = HelpSerializer


class HelpDetailView(generics.RetrieveAPIView):
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class IconHelpView(ListAPIView):
    queryset = HelpIcon.objects.all()
    serializer_class = HelpIconSerializer

    def get_serializer_context(self):
        context = super(IconHelpView, self).get_serializer_context()
        context.update({"context": self.request})
        return context
