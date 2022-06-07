from django.urls import path
from .views import CollectionAPIView, CollectionListView, ItemAPIView, \
    ItemListView, APIBasketCreateView, APIBasketDeleteAllView, APIAddBasketView, \
    APIBasketTotalPriceView, OrderCreateView, SameItemListView, \
    ItemFavouriteUpdateView, ItemRandomView

urlpatterns = [
    path('', ItemListView.as_view(), name='items-list'),
    path('<int:pk>/', ItemAPIView.as_view(), name='item-detail'),
    path('collections/', CollectionListView.as_view(), name='collections-list'),
    path('collections/<int:pk>/', CollectionAPIView.as_view(), name='collection-detail'),
    path('basket/create/', APIBasketCreateView.as_view(), name='basket-create'),
    path('basket/delete-all/', APIBasketDeleteAllView.as_view(), name='basket-delete-all'),
    path('basket/add/', APIAddBasketView.as_view(), name='basket'),
    path('basket/total/', APIBasketTotalPriceView.as_view(), name='basket-total'),
    path('same/', SameItemListView.as_view(), name='same'),
    path('order/', OrderCreateView.as_view(), name='order'),
    path('favourite/<int:pk>/', ItemFavouriteUpdateView.as_view()),
    path('random/', ItemRandomView.as_view()),

]