from django.urls import path
from .views import AboutUsView, NewsListView, NewsDetailView, OfferListView, HelpListView

urlpatterns = [
    path('about/', AboutUsView.as_view()),
    path('news/', NewsListView.as_view()),
    path('news/<int:pk>/', NewsDetailView.as_view()),
    path('offer/', OfferListView.as_view()),
    path('help/', HelpListView.as_view(),),
    path('help/<int:pk>/', HelpListView.as_view(),),

]