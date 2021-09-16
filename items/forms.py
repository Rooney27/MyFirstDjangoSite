from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        template_name = 'items/order.html'
        exclude = ['items','is_paid']