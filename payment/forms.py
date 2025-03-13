from django import forms

from .models import ShippingAddress

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on Card'}))
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}))
    card_expiry = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))
    card_cvc = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVC'}))
    card_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address'}))
    card_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    card_postal_code = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}))
    card_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    shipping_email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    shipping_address1 = forms.CharField(label="Address 1", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}))
    shipping_address2 = forms.CharField(label="Address 2", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}))
    shipping_city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    shipping_state = forms.CharField(label="State", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    shipping_postal_code = forms.CharField(label="Postal Code", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}))
    shipping_country = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country']