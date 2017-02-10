from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from customer.models import Channel, CreditCard, AddressLine
from business.serializers import CountryCurrencySerializer, CountrySerializer
from prepyme.serializers import PageSerializer, PrepymeSerializer
from cms.models import Prepyme, PageChannel


class PageChannelSerializer(serializers.ModelSerializer):
    post = PrepymeSerializer(many=False)

    class Meta:
        model = PageChannel
        fields = (
            'id', 'post', 'channel', 'amount'
        )


class ChannelSerializer(serializers.ModelSerializer):
    channel_page = PageChannelSerializer(many=True)
    country_currency_id = CountryCurrencySerializer(many=False)

    class Meta:
        model = Channel
        fields = (
            'id', 'name', 'description', 'active', 'country_currency_id', 'channel_page'
        )


class AddressLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressLine
        fields = (
            'id', 'profile_id', 'detail', 'status'
        )

