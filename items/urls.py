from django.urls import path, include
from .views import CollectionAPIView, CollectionListView, ItemAPIView, \
    ItemListView, APIBasketCreateView, APIBasketDeleteAllView, APIAddBasketView, \
    APIBasketTotalPriceView, OrderCreateView, SameItemListView, \
    ItemFavouriteUpdateView, ItemRandomView, DeleteOneAmountBasketView, DeleteByPKBasketView

urlpatterns = [
    path('', ItemListView.as_view(), name='items-list'),
    path('<int:pk>/', ItemAPIView.as_view(), name='item-detail'),
    path('collections/', CollectionListView.as_view(), name='collections-list'),
    path('collections/<int:pk>/', CollectionAPIView.as_view(), name='collection-detail'),
    path('same/', SameItemListView.as_view(), name='same'),
    path('favourite/<int:pk>/', ItemFavouriteUpdateView.as_view()),
    path('random/', ItemRandomView.as_view()),

]

basket_url = [
    path('basket/create/', APIBasketCreateView.as_view(), name='basket-create'),
    path('basket/delete-all/', APIBasketDeleteAllView.as_view(), name='basket-delete-all'),
    path('basket/add/', APIAddBasketView.as_view(), name='basket'),
    path('basket/del/', DeleteOneAmountBasketView.as_view(), name='basket-del'),
    path('basket/total/', APIBasketTotalPriceView.as_view(), name='basket-total'),
    path('basket/remove/<int:pk>/', DeleteByPKBasketView.as_view(), name='basket-total'),
    path('order/', OrderCreateView.as_view(), name='order'),

]

urlpatterns += basket_url
