from django.urls import path, include
from .views import CollectionAPIView, CollectionListView, ItemAPIView, \
    ItemListView, APIBasketCreateView, APIBasketDeleteAllView, APIAddBasketView, \
    APIBasketTotalPriceView, OrderCreateView, SameItemListView, \
    ItemRandomView, DeleteOneAmountBasketView, DeleteByPKBasketView, OrderListView, \
    OrderDetailView, NoveltyItemView, UserFavouriteList, UserFavouriteCreate, ItemFavoriteDestroyByItemView

urlpatterns = [
    path('', ItemListView.as_view(), name='items-list'),
    path('<int:pk>/', ItemAPIView.as_view(), name='item-detail'),
    path('collections/', CollectionListView.as_view(), name='collections-list'),
    path('collections/<int:pk>/', CollectionAPIView.as_view(), name='collection-detail'),
    path('same/', SameItemListView.as_view(), name='same'),
    path('random/', ItemRandomView.as_view()),
    path('novelty/', NoveltyItemView.as_view()),
    path('favourite/', UserFavouriteList.as_view()),
    path('favourite/create/', UserFavouriteCreate.as_view()),
    path('favourite/delete/', ItemFavoriteDestroyByItemView.as_view()),
]

basket_order_url = [
    path('basket/create/', APIBasketCreateView.as_view(), name='basket-create'),
    path('basket/delete-all/', APIBasketDeleteAllView.as_view(), name='basket-delete-all'),
    path('basket/add/', APIAddBasketView.as_view(), name='basket'),
    path('basket/del/', DeleteOneAmountBasketView.as_view(), name='basket-del'),
    path('basket/total/', APIBasketTotalPriceView.as_view(), name='basket-total'),
    path('basket/remove/<int:pk>/', DeleteByPKBasketView.as_view(), name='basket-total'),
    path('order/create/', OrderCreateView.as_view(), name='order'),
    path('order/', OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-list'),

]

urlpatterns += basket_order_url
