from django.contrib import admin
from customer.models import CreditCard
from customer.forms import CreditCardForm


class CreditCardAdmin(admin.ModelAdmin):
    exclude = ['updated_at']
    form = CreditCardForm

admin.site.register(CreditCard, CreditCardAdmin)