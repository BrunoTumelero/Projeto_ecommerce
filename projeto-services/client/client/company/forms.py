from django import forms

from client.register.models import CompanySpecialty, Products

class CompanySpecialtyForm(forms.ModelForm):

    class Meta:
        model = CompanySpecialty
        fields = ['specialty', 'sub_specialty']

class ProductsForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'