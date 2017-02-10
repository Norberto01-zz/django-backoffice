from rest_framework import serializers
from business.models import Currency, Country, CountryCurrency, ChannelAmounts
from cms.models import AmountNode
from customer.models import Channel


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id', 'name', 'print_name', 'iso2', 'iso3', 'country_code', 'region'
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'id', 'name', 'code', 'symbol', 'code'
        )


class CountryCurrencySerializer(serializers.ModelSerializer):
    country_id = CountrySerializer(many=False)
    currency_id = CurrencySerializer(many=False)

    class Meta:
        model = CountryCurrency
        fields = (
            'id', 'country_id', 'currency_id'
        )


class AmountNodeSerializer(serializers.ModelSerializer):
    class Channels(serializers.ModelSerializer):
        country_currency_id = CountryCurrencySerializer(many=False)

        class Meta:
            model = Channel
            fields = (
                'id', 'name', 'country_currency_id'
            )
    channel = Channels(many=False)

    class Meta:
        model = AmountNode
        fields = (
            'id', 'amount_label', 'channel', 'amount'
        )


class ChannelAmountsSerializer(serializers.ModelSerializer):
    rel_channel_amounts = AmountNodeSerializer(many=True)

    class Meta:
        model = ChannelAmounts
        fields = (
            'id', 'title', 'rel_channel_amounts'
        )