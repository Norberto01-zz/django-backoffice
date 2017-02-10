from rest_framework.viewsets import ModelViewSet
from business.models import Currency, Country, ChannelAmounts
from business.serializers import CountrySerializer, CurrencySerializer, ChannelAmountsSerializer


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ChannelAmountsViewSet(ModelViewSet):
    queryset = ChannelAmounts.objects.filter(active=True)
    serializer_class = ChannelAmountsSerializer
