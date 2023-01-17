from django import forms

from client.register.models import ConsumersCards

class ConsumersCardsForm(forms.ModelForm):

    class Meta:
        model = ConsumersCards
        fields = ['consumer_name', 'card_number', 'cod_card', 'expiration_date', 'flag_card']