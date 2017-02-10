from django.conf.urls import include, url
from rest_framework import routers
from business.views import (CurrencyViewSet, CountryViewSet)

router = routers.DefaultRouter()

router.register(r'currencies', CurrencyViewSet)
router.register(r'countries', CountryViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
