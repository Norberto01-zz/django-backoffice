from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import Pages, PageChannel
from customer.serializers import ChannelSerializer


class RelatedChannelSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(many=False)

    class Meta:
        model = PageChannel
        fields = (
            'id', 'amount', 'channel'
        )


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class RatesSerializer(serializers.ModelSerializer):
    related_channel_page = RelatedChannelSerializer(many=True)

    class Meta:
        model = Pages
        fields = (
            'id', 'title', 'cat', 'slug', 'live', 'related_channel_page'
        )



class RatesAmountSerializer(RatesSerializer):

    class Meta(RatesSerializer.Meta):
        model = Pages
        fields = RatesSerializer.Meta.fields + (
            'amount', 'channel',
        )


class RatesCountryItemSerializer(RatesSerializer):
    children = RatesAmountSerializer(many=True)

    class Meta(RatesSerializer.Meta):
        model = Pages
        fields = RatesSerializer.Meta.fields + (
            'children',
        )


class RatesCountrySerializer(RatesSerializer):
    children = RatesCountryItemSerializer(many=True)

    class Meta(RatesSerializer.Meta):
        model = Pages
        fields = RatesSerializer.Meta.fields + (
            'country', 'children',
        )


class RatesImportSerializer(RatesSerializer):
    children = RatesCountrySerializer(many=True)

    class Meta(RatesSerializer.Meta):
        model = Pages
        fields = RatesSerializer.Meta.fields + (
            'document', 'children'
        )
