from django import forms

from client.register.models import State, City, CompanySpecialty, ProductCategory

class StateForm(forms.ModelForm):

    class Meta:
        model = State
        fields = ['uf', 'name']

class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ['name', 'state']

class CompanySpecialtyForm(forms.ModelForm):

    class Meta:
        model = CompanySpecialty
        fields = ['specialty', 'sub_specialty']

class ProductCategoryForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = ['category', 'description']