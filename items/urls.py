from django.urls import path
from .views import CollectionAPIView, CollectionListView, CollectionCreateView, ItemAPIView, \
    ItemCreateView, ItemListView, APIBasketCreateView

urlpatterns = [
    path('', ItemListView.as_view()),
    path('<int:pk>/', ItemAPIView.as_view()),
    path('create/', ItemCreateView.as_view()),
    path('collections/create/', CollectionCreateView.as_view()),
    path('collections/', CollectionListView.as_view()),
    path('collections/<int:pk>/', CollectionAPIView.as_view()),
    path('basket/create/', APIBasketCreateView.as_view()),

]