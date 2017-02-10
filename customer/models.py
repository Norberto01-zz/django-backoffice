from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from wagtail.wagtailsnippets.models import register_snippet
from customer.forms import CreditCardForm
import pprint
import uuid
import datetime
import time


@register_snippet
class Channel(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=255, null=False)
    description = models.CharField(verbose_name=_("Description"), max_length=255, null=True, blank=True)
    country_currency_id = models.ForeignKey(
        'business.CountryCurrency',
        default=1,
        null=False,
        on_delete=models.SET_DEFAULT,
        related_name='channel_cc_id'
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'


# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    card_id = models.CharField(verbose_name=_("Card Id"), max_length=80, null=True, default=None)
    pin = models.CharField(verbose_name=_("Pin"), max_length=80, null=True, default=None)
    sms_verified = models.BooleanField(verbose_name=_("Sms Verified"), default=False)
    city = models.CharField(verbose_name=_("City"), max_length=280, null=True, blank=True)
    zip_code = models.CharField(verbose_name=_("Zip Code"), max_length=10, null=True, blank=True)
    mobile = models.CharField(verbose_name=_("Mobile"), max_length=15, null=True, blank=True)
    address_line1 = models.CharField(verbose_name=_("Address Line 1"), max_length=280, null=True, blank=True)
    address_line2 = models.CharField(verbose_name=_("Address Line 2"), max_length=280, null=True, blank=True)
    signup_token = models.CharField(verbose_name=_("Signup Token"), max_length=280, null=True)
    sifts_last_update = models.DateField(verbose_name=_("Sifts Update"), default=now)
    sifts_score = models.FloatField(verbose_name=_("Sifts Score"), default=0.0)
    channel = models.ForeignKey(
        'customer.Channel',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_DEFAULT,
        related_name='profile_channel_id'
    )
    country = models.ForeignKey(
        'business.Country',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_DEFAULT,
        related_name='country_profile_id'
    )

    status_profile = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now)

    # def clean(self):
    #     if not self.signup_token:
    #         self.signup_token = uuid.uuid1().hex

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.signup_token = uuid.uuid1().hex
    #     return super(Profile, self).save(*args, **kwargs)


# Hook to the user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile.signup_token = uuid.uuid1().hex
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    pp = pprint.PrettyPrinter(depth=6)
    if not instance.profile.signup_token:
        name = str(uuid.uuid4())+instance.username+str(uuid.uuid1())
        instance.profile.signup_token = uuid.uuid5(uuid.NAMESPACE_DNS, name).hex

    pp.pprint(instance.profile.signup_token)
    instance.profile.save()


class Phone(models.Model):
    profile_id = models.ForeignKey(
        User,
        default=None,
        null=True,
        on_delete=models.SET_DEFAULT,
        related_name='phone_profile_id'
    )
    phone = models.CharField(verbose_name=_("Phone"), max_length=15, null=False)

    status_phone = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now)


@register_snippet
class CreditCardType(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=80, null=False)
    status_cc_type = models.BooleanField(default=True)

    def __str__(self):
        return self.name

YEARMONTH_INPUT_FORMATS = (
    '%Y-%m', '%m/%Y', '%m/%y', # '2017-10', '10/2017', '10/17'
)


class YearMonthField(models.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid year and month.'),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super(YearMonthField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats

    def clean(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return format(value, '%Y-%m')
        if isinstance(value, datetime.date):
            return format(value, '%Y-%m')
        for fmt in self.input_formats or YEARMONTH_INPUT_FORMATS:
            try:
                date = datetime.date(*time.strptime(value, fmt)[:3])
                return format(date, '%Y-%m')
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])


@register_snippet
class CreditCard(models.Model):
    profile_id = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=False,
        on_delete=models.SET_DEFAULT,
        related_name='profile_cc_id'
    )
    # expired_on = models.DateField(default=now, null=False)
    expired_year = models.CharField(verbose_name=_("Expired CC Year"), max_length=4, default='', blank=True)
    expired_month = models.CharField(verbose_name=_("Expired CC Month"), max_length=2, default='', blank=True)
    card_holder_name = models.CharField(verbose_name=_("Card Holder Name"), max_length=80, null=False)
    cvv_number = models.CharField(verbose_name=_("CVV Number"), max_length=4, null=True, blank=True, default='')
    cc_number = models.CharField(verbose_name=_("Credit Card Number"), max_length=16, null=False, unique=True)
    cc_type_id = models.ForeignKey(
        'customer.CreditCardType',
        default=1,
        null=False,
        blank=False,
        on_delete=models.SET_DEFAULT,
        related_name='cc_cct_id'
    )
    address_line = models.ForeignKey(
        "customer.AddressLine",
        default=None,
        null=True,
        blank=False,
        on_delete=models.SET_DEFAULT,
        related_name='profile_cc_id'
    )
    status_cc = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now)

    base_form_class = CreditCardForm

    def __str__(self):
        return "%s - %s - %s" % (self.profile_id, self.card_holder_name, self.cc_number)

    def get_context(self, request):
        context = super(CreditCard, self).get_context(request)
        pp = pprint.PrettyPrinter(depth=6) 
        pp.pprint(context['address_line'])
        return context


@register_snippet
class AddressLine(models.Model):
    profile_id = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=False,
        on_delete=models.SET_DEFAULT,
        related_name='profile_ba_id'
    )
    detail = models.TextField(verbose_name=_("Detail"), null=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.profile_id, self.detail)
