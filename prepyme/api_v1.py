from django.conf.urls import include, url
# from rest_framework import routers
from .routers import DefaultRouter
from prepyme.views import (UserViewSet, GroupViewSet, PrepymeViewSet, ImageViewSet)
from cms.views import RateImportViewSet, RateCountryViewSet
from business.views import (CurrencyViewSet, CountryViewSet, ChannelAmountsViewSet)
from customer.views import ChannelViewSet, CreditCardViewSet, AddressLineViewSet

router = DefaultRouter()

# router.register(r'phoneval/(?P<number>[0-9]+)/$', PhoneValVieset.phone)
router.register(r'rates', RateCountryViewSet)
# router.register(r'amounts', RatesAmountViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'prepyges', PrepymeViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'images', ImageViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'amounts', ChannelAmountsViewSet)
router.register(r'creditcards', CreditCardViewSet)
router.register(r'addresses', AddressLineViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
