from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import AboutUs, News, Help, Offer, Contacts, MainPageIcon, Advantages, CallBack, HelpIcon, HeaderFooterPic
from .serializers import AboutSerializer, NewsSerializer, HelpSerializer, OfferSerializer, \
    ContactsSerializer, MainPageIconSerializer, AdvantagesSerializer, CallBackSerializer, HeaderFooterPicSerializer
from rest_framework import generics


class CustomPagination(PageNumberPagination):
    """class for pagination"""

    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CallBackView(generics.CreateAPIView):
    """view for create callback """

    queryset = CallBack.objects.all()
    serializer_class = CallBackSerializer


class ContactView(generics.ListAPIView):
    """view for show social pages, administration contacts
    and picture for header and footer"""

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class HeaderFooterView(generics.ListAPIView):
    """view for show social pages, administration contacts
    and picture for header and footer"""

    queryset = HeaderFooterPic.objects.all()
    serializer_class = HeaderFooterPicSerializer


class MainPageView(generics.ListAPIView):
    """view for list slider in main page"""

    queryset = MainPageIcon.objects.all()
    serializer_class = MainPageIconSerializer


class AdvantagesView(generics.ListAPIView):
    """view for list zeon store's advantages"""

    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer


class AboutUsView(generics.ListAPIView):
    """get information about company"""

    queryset = AboutUs.objects.all()
    serializer_class = AboutSerializer


class NewsView(generics.ListAPIView):
    """get list news information in company"""

    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    pagination_class = CustomPagination


class NewsViewDetail(generics.RetrieveAPIView):
    """get detail news information in company"""

    queryset = News.objects.all()
    serializer_class = NewsSerializer


class OfferView(generics.ListAPIView):
    """get public company's offer"""

    queryset = Offer.objects.all().order_by('-id')
    serializer_class = OfferSerializer


class HelpView(generics.ListAPIView):
    """get list help information"""

    queryset = Help.objects.all().order_by('-id')
    serializer_class = HelpSerializer

    def get_serializer_context(self):
        context = super(HelpView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


class HelpDetailView(generics.RetrieveAPIView):
    """het detail help information"""

    queryset = Help.objects.all()
    serializer_class = HelpSerializer

    def get_serializer_context(self):
        context = super(HelpDetailView, self).get_serializer_context()
        context.update({"context": self.request})
        return context


