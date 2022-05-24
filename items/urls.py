from django.urls import path
from .views import CollectionAPIView, CollectionListView, CollectionCreateView, ItemAPIView, \
    ItemCreateView, ItemListView

urlpatterns = [
    path('', ItemListView.as_view()),
    path('<int:pk>/', ItemAPIView.as_view()),
    path('create/', ItemCreateView.as_view()),
    path('collections/create/', CollectionCreateView.as_view()),
    path('collection/', CollectionListView.as_view()),
    path('collection/<int:pk>/', CollectionAPIView.as_view()),

]