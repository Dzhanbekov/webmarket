from django.urls import path, include
from .views import AboutUsViewSet, NewsViewSet, OfferViewSet, HelpViewSet, \
    ContactViewSet, AdvantagesViewSet, MainPageViewSet, CallBackViewSet, IconHelpView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('about', AboutUsViewSet)
router.register('news', NewsViewSet)
router.register('offer', OfferViewSet)
router.register('help', HelpViewSet)
router.register('contact', ContactViewSet)
router.register('advantages', AdvantagesViewSet)
router.register('slider', MainPageViewSet)
router.register('callback', CallBackViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('icon/', IconHelpView.as_view()),

]
