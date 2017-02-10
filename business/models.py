from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.models import register_snippet
from cms.models import PageChannel
from django.contrib.auth.models import User


@register_snippet
class Country(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=255, null=True, blank=True)
    print_name = models.CharField(verbose_name=_("print_name"), max_length=255, null=True, blank=True)
    iso2 = models.CharField(verbose_name=_("ISO 2"), max_length=255, null=True, blank=True)
    iso3 = models.CharField(verbose_name=_("ISO 3"), max_length=255, null=True, blank=True)
    country_code = models.PositiveIntegerField(verbose_name=_("Country Code"), null=True, blank=True)
    region = models.CharField(verbose_name=_("region"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


@register_snippet
class Currency(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=255, null=True, blank=True)
    code = models.CharField(verbose_name=_("Code"), max_length=5, null=True, blank=True)
    symbol = models.CharField(verbose_name=_("Symbol"), max_length=10, null=True, blank=True)
    country_id = models.ForeignKey(
        'business.Country',
        null=False,
        on_delete=models.CASCADE,
        related_name='country'
    )

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name


@register_snippet
class CountryCurrency(models.Model):
    country_id = models.ForeignKey(
        'business.Country',
        null=False,
        on_delete=models.CASCADE,
        related_name='country_id'
    )
    currency_id = models.ForeignKey(
        'business.Currency',
        null=False,
        on_delete=models.CASCADE,
        related_name='currency_id'
    )

    def __str__(self):
        return str(self.country_id) + " - " + str(self.currency_id)

# class ModelA():
#     property = foo
#
#     panels = [
#         FieldPanel('blah')
#         InlinePanel(ModelA, 'relationship_model')
#     ]
#
# class ModelB():
#     property = bar
#
# class ModelC():
#     property = models.ForeignKey(ModelB)
#     page = ParentalKey(ModelA, related_name='relationship_model')
#
#     panels = [
#         FieldPanel('property')
#     ]
#-----------------------------------------------------------------------------


class PinlessAmounts(Page):
    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['business.ChannelAmounts']
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    @classmethod
    def can_create_at(cls, parent):
        return super(PinlessAmounts, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        verbose_name = 'Pinless Amount Group'
        verbose_name_plural = 'Pinless Amounts Groups'

    content_panels = [
        FieldPanel('title'),
        FieldPanel('active')
    ]


class ChannelAmounts(Page):
    parent_page_types = ['business.PinlessAmounts']
    subpage_types = []
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Channel Amount Item'
        verbose_name_plural = 'Channels Amounts Items'

    content_panels = [
        FieldPanel('title'),
        FieldPanel('active'),
        InlinePanel('rel_channel_amounts', label="Related Channel Amounts", max_num=2, min_num=1)
    ]

    # @classmethod
    # def can_create_at(cls, parent):
    #     return super(ChannelAmounts, cls).can_create_at(parent) and not cls.objects.exists()

#----------------------------------------------------------------------------------------------


class PaymentMethod(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=80, null=False)
    description = models.TextField(verbose_name=_("Description"), max_length=300, null=True, blank=True)

    status_method = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now)


class Payment(models.Model):
    amount = models.FloatField(verbose_name=_("Amount"))
    credit_card = models.ForeignKey(
        'customer.CreditCard',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_DEFAULT,
        related_name='payment_cc_id'
    )
    method = models.ForeignKey(
        'business.PaymentMethod',
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_DEFAULT,
        related_name='payment_method_id'
    )

    status_payment = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now, null=True)


class Service(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=80, null=False)
    description = models.TextField(verbose_name=_("Description"), max_length=300, null=True, blank=True)

    status_service = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now)


class Operator(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=80, null=False)
    code = models.CharField(verbose_name=_("Code"), max_length=20, null=False)

    status_operator = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(default=now)


class Transaction(models.Model):
    service = models.ForeignKey(
        'business.Service',
        null=False,
        related_name='transaction_service_id'
    )
    payment = models.ForeignKey(
        'business.Payment',
        null=True,
        related_name='transaction_payment_id'
    )
    user = models.ForeignKey(User, related_name='owner_transaction')
    # amount_rate_id = models.ForeignKey(
    #     'cms.AmountRate',
    #     default=None,
    #     null=False,
    #     related_name='transaction_rates_id'
    # )
    transaction_code = models.CharField(verbose_name=_("Transaction Code"), max_length=20)
    next_transaction_date = models.DateTimeField(null=True)
    next_unit_day = models.PositiveIntegerField(verbose_name=_("Next Unit Day"), default=None, null=True)
    related_transaction = models.ForeignKey(
        'business.Transaction',
        null=True,
        related_name='transaction_related_id'
    )
    status_transaction = models.ForeignKey(
        'business.TransactionStatus',
        null=True,
        related_name='+'
    )
    created_at = models.DateTimeField(auto_now=True)


class TransactionStatus(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=20)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SystemLog(models.Model):
    transaction_id = models.ForeignKey(
        'business.Transaction',
        null=False,
        related_name='system_transaction_id'
    )
    description = models.TextField(verbose_name=_("Description"), max_length=600, null=True, blank=True)
    session_id = models.TextField(verbose_name=_("Session"), max_length=600, null=False)
    user_agent_id = models.TextField(verbose_name=_("User Agent Id"), max_length=600, null=False)
    request = models.TextField(verbose_name=_("Request"), max_length=600, null=True, blank=True)
    response = models.TextField(verbose_name=_("Response"), max_length=600, null=True, blank=True)


class TransactionDetail(models.Model):
    transaction_id = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True
    )
    operator = models.PositiveIntegerField(null=True)
    country = models.PositiveIntegerField(null=True)
    destination_amount = models.FloatField(verbose_name=_("Destination amount"))
    phone_number = models.CharField(verbose_name=_("Phone number"), max_length=15)
    description = models.TextField(verbose_name=_("Description"), max_length=600, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

