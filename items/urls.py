from django.urls import path
from .views import CollectionAPIView, CollectionListView, CollectionCreateView, ItemAPIView, \
    ItemCreateView, ItemListView, APIBasketCreateView, APIBasketDeleteAllView, APIAddBasketView, \
    APIBasketTotalPriceView, APIBasketTotalQuantityView, NoveltyListView, OrderCreateView, SameItemListView, \
    SearchHelperView, ItemFavouriteAPIView

urlpatterns = [
    path('', ItemListView.as_view(), name='items-list'),
    path('<int:pk>/', ItemAPIView.as_view(), name='item-detail'),
    path('create/', ItemCreateView.as_view(), name='item-create'),
    path('collections/create/', CollectionCreateView.as_view(), name='collection-create'),
    path('collections/', CollectionListView.as_view(), name='collections-list'),
    path('collections/<int:pk>/', CollectionAPIView.as_view(), name='collection-detail'),
    path('basket/create/', APIBasketCreateView.as_view(), name='basket-create'),
    path('basket/delete-all/', APIBasketDeleteAllView.as_view(), name='basket-delete-all'),
    path('basket/add/', APIAddBasketView.as_view(), name='basket'),
    path('basket/total-price/', APIBasketTotalPriceView.as_view(), name='basket-total-price'),
    path('basket/total-quantity/', APIBasketTotalQuantityView.as_view(), name='basket-total-quantity'),
    path('novelty/', NoveltyListView.as_view(), name='novelty'),
    path('same/', SameItemListView.as_view(), name='same'),
    path('order/', OrderCreateView.as_view(), name='order'),
    path('search/helper/', SearchHelperView.as_view()),
    path('favourite/<int:pk>/', ItemFavouriteAPIView.as_view()),

]