from wagtail.wagtailadmin.forms import WagtailAdminPageForm
from django import forms
import pprint
from django.contrib.sessions.models import Session
from importlib import import_module
from django.conf import settings


class CreditCardForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        # SessionData = import_module(settings.SESSION_ENGINE).SessionStore
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint("%s --> ARGS...")
        super(CreditCardForm, self).__init__(*args, **kwargs)
