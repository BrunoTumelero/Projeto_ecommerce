from django import forms

from client.register.models import Products, Shopping_Cart, Whishes

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ['company', 'product_name', 'product_description', 'product_category', 'product_price', 'is_avalable']

class ShoppingCartForm(forms.ModelForm):

    class Meta:
        model = Shopping_Cart
        fields = ['consumer', 'product', 'amount', 'selected']

class WhishesForm(forms.ModelForm):

    class Meta:
        model = Whishes
        fields = ['consumer', 'product', 'annotation', 'amount', 'priority']