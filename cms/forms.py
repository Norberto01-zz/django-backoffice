from django import forms
from wagtail.wagtailadmin.forms import WagtailAdminPageForm
import pprint
from django.forms.models import modelform_factory, ModelForm
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from django.utils.translation import ugettext_lazy as _
import time


class PrePageForm(WagtailAdminPageForm, forms.Form):
    def __init__(self, *args, **kwargs):

        pp = pprint.PrettyPrinter(depth=6)

        super(PrePageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        prepy = super(PrePageForm, self).save(commit=False)

        if commit:
            prepy.save()
        return prepy
