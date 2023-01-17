from django import forms

from client.register.models import CompanySpecialty

class CompanySpecialtyForm(forms.ModelForm):

    class Meta:
        model = CompanySpecialty
        fields = ['specialty', 'sub_specialty']