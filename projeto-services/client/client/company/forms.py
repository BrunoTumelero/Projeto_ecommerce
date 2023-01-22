from django import forms

from client.register.models import Products

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ['company', 'product_name', 'product_category', 'product_price', 'is_avalable']