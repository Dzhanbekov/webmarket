from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import AboutUs, News, Help, Offer, Contacts, MainPageIcon, Advantages, CallBack, HelpIcon
from .serializers import AboutSerializer, NewsSerializer, HelpSerializer, OfferSerializer, \
    ContactsSerializer, MainPageIconSerializer, AdvantagesSerializer, CallBackSerializer, HelpIconSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class CustomPagination(PageNumberPagination):
    '''class for pagination'''

    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CallBackViewSet(viewsets.ModelViewSet):
    """function for callback's all http methods"""

    queryset = CallBack.objects.all()
    serializer_class = CallBackSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """function for contact's all http methods"""

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class MainPageViewSet(viewsets.ModelViewSet):
    """function for main pages all http methods"""

    queryset = MainPageIcon.objects.all()
    serializer_class = MainPageIconSerializer


class AdvantagesViewSet(viewsets.ModelViewSet):
    """function for advantages all http methods"""

    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer


class AboutUsViewSet(viewsets.ModelViewSet):
    """function for about uses all http methods"""

    queryset = AboutUs.objects.all()
    serializer_class = AboutSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    pagination_class = CustomPagination


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-id')
    serializer_class = OfferSerializer


class HelpViewSet(viewsets.ModelViewSet):
    queryset = Help.objects.all().order_by('-id')
    serializer_class = HelpSerializer


class IconHelpView(ListAPIView):
    queryset = HelpIcon.objects.all()
    serializer_class = HelpIconSerializer

    def get_serializer_context(self):
        context = super(IconHelpView, self).get_serializer_context()
        context.update({"context": self.request})
        return context
