from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.contrib.auth.models import Group
from wagtail.wagtailcore.models import Page
from cms.models import Prepyme, PrepyImage, Pages
from customer.models import CreditCard, AddressLine
import pprint
# from business.serializers import CountryCurrencySerializer


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = (
            'id', 'profile_id', 'expired_year', 'expired_month', 'card_holder_name', 'cvv_number', 'cc_number', 'cc_type_id',
            'status_cc', 'address_line'
        )


class UserSerializer(serializers.ModelSerializer):
    card_id = serializers.CharField(source='profile.card_id', allow_blank=True, allow_null=True)
    pin = serializers.CharField(source='profile.pin', allow_blank=True, allow_null=True)
    country = serializers.CharField(source='profile.country', allow_blank=True, allow_null=True)
    mobile = serializers.CharField(source='profile.mobile', allow_blank=True, allow_null=True)
    address_line = serializers.CharField(source='profile.address_line1', allow_blank=True, allow_null=True)
    zipcode = serializers.CharField(source='profile.zip_code', allow_blank=True, allow_null=True)
    city = serializers.CharField(source='profile.city', allow_blank=True, allow_null=True)
    signup_token = serializers.CharField(source='profile.signup_token', read_only=True)

    channel = serializers.IntegerField(source='profile.channel.pk', allow_null=True)

    sms_verified = serializers.BooleanField(source='profile.sms_verified', default=False)
    status_profile = serializers.BooleanField(source='profile.status_profile', default=True)
    profile_cc_id = CreditCardSerializer(many=True, read_only=True)
    # address_line = serializers.IntegerField(source='profile.country_id')

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'card_id', 'pin', 'channel', 'country',
            'sms_verified', 'status_profile', 'mobile', 'address_line', 'zipcode', 'city', 'signup_token',
            'profile_cc_id'
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        profile = instance.profile
        profile.address_line1 = profile_data['address_line1']
        profile.card_id = profile_data['card_id']
        profile.pin = profile_data['pin']
        # profile.channel = profile_data['channel']
        profile.mobile = profile_data['mobile']
        profile.zip_code = profile_data['zip_code']
        profile.city = profile_data['city']
        profile.sms_verified = profile_data['sms_verified']

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        profile.save()

        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = authenticate(username=data['username'], password=data['password'])
            if user and user.is_active:
                data['user'] = user
                return data
        except get_user_model().DoesNotExist:
            pass
        raise serializers.ValidationError('Wrong username or password')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'url', 'name'
        )


class ImageSerializer(serializers.ModelSerializer):
    # snip = serializers.StringRelatedField(many=False)
    class Meta:
        model = PrepyImage
        fields = (
            'id', 'title', 'file', 'caption', 'snip'
        )


class PageSerializer(serializers.ModelSerializer):
    main_image = ImageSerializer(many=False, read_only=True)

    class Meta:
        model = Page
        fields = (
            'id', 'title', 'slug', 'main_image', 'show_in_menus'
        )


class PagesSerializer(PageSerializer):
    class Meta(PageSerializer.Meta):
        model = Pages
        fields = PageSerializer.Meta.fields


class PrepymeSerializer(PagesSerializer):
    # main_image = ImageSerializer(many=False, read_only=True)
    cat = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    # body = serializers.StringRelatedField(many=True)
    # tags = serializers.StringRelatedField(many=True)
    children = PagesSerializer(many=True, read_only=True)
    parent = PagesSerializer(many=False, read_only=True)
    # amount = serializers.FloatField()

    class Meta(PagesSerializer.Meta):
        model = Prepyme
        fields = PagesSerializer.Meta.fields + (
            'show_in_menus', 'cat', 'parent', 'children'
        )


