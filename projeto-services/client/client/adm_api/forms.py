from django import forms

from client.register.models import State, City, CompanySpecialty, ProductCategory, SubCategory, Permission

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

class ProductSubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = ['category', 'sub_category', 'description']
        
class PermissionForm(forms.ModelForm):

    class Meta:
        model = Permission
        fields = ['permission_name', 'description']