from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, InlinePanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsearch import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from django.db.models.signals import pre_delete, pre_save
from wagtail.wagtaildocs.models import AbstractDocument
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
import pprint
from cms.forms import PrePageForm
import csv
import os.path

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class AbsSnippet(models.Model):
    url = models.URLField(null=True, blank=True)
    text = models.CharField(verbose_name=_("Label"), max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    search_fields = [
        index.SearchField('text', partial_match=True),
    ]

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


# class ImageCategory
@register_snippet
class ImageCategory(AbsSnippet):
    class Meta:
        verbose_name = 'Image Snip'
        verbose_name_plural = 'Image Snips'


# ----------------------- MY CUSTOM IMAGE MODEL -----------------------------------------------------------------
class PrepyImage(AbstractImage):
    DEFAULT_IMG_ID = 1
    caption = models.CharField(verbose_name=_("Caption"), max_length=255, null=True, blank=True)
    snip = models.ForeignKey(
        'cms.ImageCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        default=DEFAULT_IMG_ID
    )
    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        'caption',
        'snip'
    )

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
    ]


class PrepyRendition(AbstractRendition):
    image = models.ForeignKey(PrepyImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=PrepyImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=PrepyRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# @receiver(pre_saveSl_point(instance.get_suggested_focal_point())

# ------------------------------MY CUSTOM DOCUMENT MODEL --------------------------------------------------------------
class PrepyDocs(AbstractDocument, models.Model):
    to_render = models.BooleanField(verbose_name=_("Renderize"), default=False)
    active = models.BooleanField(verbose_name=_("Current rate"), default=False)
    currency = models.ForeignKey(
        'business.Currency',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    admin_form_fields = (
        'title',
        'file',
        'collection',
        'tags',
        'to_render',
        'currency',
        'active',
    )

    def save(self, *args, **kwargs):
        predocs = super(PrepyDocs, self).save(*args, **kwargs)
        pp = pprint.PrettyPrinter(depth=6)
        if self.to_render and self.pk:
            pp.pprint("Rendering self.file to webservice...")
            pp.pprint(self.file.path)
            ext = os.path.splitext(self.file.path)[1]
            if ext in ['.csv', '.xlsx', '.xls', '.xml']:
                pp.pprint(ext)
                pp.pprint("Extension valida!")
                with open(str(self.file.path)) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        pp.pprint(row)
            else:
                pp.pprint("Extension invalida!")
        else:
            pp.pprint("To render is not true go & save...")
        return predocs


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=PrepyDocs)
def document_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


# ---------------------------------------------------------------------------------------------------------------------
class WebServiceOperators(models.Model):
    iso_country = models.CharField(verbose_name=_("ISO 2"), max_length=255, null=True, blank=True)
    iso_operator = models.CharField(verbose_name=_("Operator"), max_length=255, null=True, blank=True)
    operator_name = models.CharField(verbose_name=_("Operator Name"), max_length=255, null=True, blank=True)
    prefix = models.CharField(verbose_name=_("Operator Name"), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.operator_name


# class Category
@register_snippet
class Category(AbsSnippet):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class PrePageTag(TaggedItemBase):
    content_object = ParentalKey('cms.Prepyme', related_name='tagged_items')


class AmountNode(Orderable):
    channel_amount = ParentalKey(
        'business.ChannelAmounts', related_name='rel_channel_amounts'
    )
    channel = models.ForeignKey(
        'customer.Channel',
        verbose_name='Service Channel',
        related_name='amount_channel'
    )
    amount_label = models.CharField(
        verbose_name=_("Label Amount"), max_length=15, default=channel.name
    )
    amount = models.PositiveIntegerField(verbose_name=_("Amount"), default=0.0)
    panels = [
        FieldPanel('amount_label'),
        FieldPanel('channel'),
        FieldPanel('amount')
    ]


class PageChannel(Orderable):
    post = ParentalKey(
        'cms.Prepyme', related_name='related_channel_page'
    )
    channel = models.ForeignKey(
        'customer.Channel',
        verbose_name='Service Channel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='channel_page'
    )
    amount = models.FloatField(verbose_name=_("Amount"), default=0.0)

    panels = [
        FieldPanel('channel'),
        FieldPanel('amount')
    ]


class Prepyme(Page):
    subpage_types = ['cms.Pages']

    parent = ParentalKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    body = StreamField([
        ('Heading', blocks.CharBlock(classname="field heading")),
        ('Paragraph', blocks.RichTextBlock()),
        ('Image', ImageChooserBlock()),
    ])
    main_image = models.ForeignKey(
        'cms.PrepyImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    document = models.ForeignKey(
        'cms.PrepyDocs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cat = models.ForeignKey(
        'cms.Category',
        verbose_name=_("Category"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    country = models.ForeignKey(
        'business.Country',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=PrePageTag, blank=True)

    class Meta:
        verbose_name = 'Root Page'
        verbose_name_plural = 'Root Pages'

    content_panels = Page.content_panels + [
        # FieldPanel('parent'),
        ImageChooserPanel('main_image'),
        DocumentChooserPanel('document'),
        SnippetChooserPanel('cat'),
        FieldPanel('country'),
        InlinePanel('related_channel_page', label="Related Channel", max_num=2),
        StreamFieldPanel('body'),
        FieldPanel('tags'),
    ]
    base_form_class = PrePageForm

    def save(self, *args, **kwargs):
        parent = self.get_parent()
        self.parent = Page.objects.get(pk=parent.pk)
        super(Prepyme, self).save(*args, **kwargs)


class Pages(Prepyme):
    parent_page_types = ['cms.Prepyme', 'cms.Pages']
    subpage_types = ['cms.Pages']

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'


class Promotion(Prepyme):
    parent_page_types = ['cms.Pages']
    subpage_types = ['cms.Pages']

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
