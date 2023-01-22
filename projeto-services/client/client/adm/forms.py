from django import forms

from client.register.models import State, City

class StateForm(forms.ModelForm):

    class Meta:
        model = State
        fields = ['uf', 'name']

class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ['name', 'state']