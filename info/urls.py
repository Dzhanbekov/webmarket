from django.urls import path, include
from .views import AboutUsView, NewsView, OfferView, HelpView, \
    ContactView, AdvantagesView, MainPageView, CallBackView, IconHelpView, NewsViewDetail, HelpDetailView

urlpatterns = [
    path('icon/', IconHelpView.as_view()),
    path('about/', AboutUsView.as_view()),
    path('news/', NewsView.as_view()),
    path('news/<int:pk>/', NewsViewDetail.as_view()),
    path('offer/', OfferView.as_view()),
    path('help/', HelpView.as_view()),
    path('help/<int:pk>/', HelpDetailView.as_view()),
    path('contact/', ContactView.as_view()),
    path('advantages/', AdvantagesView.as_view()),
    path('slider/', MainPageView.as_view()),
    path('callback/', CallBackView.as_view()),

]
