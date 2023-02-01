from django import forms

from client.register.models import ConsumersCards, Whishes

class ConsumersCardsForm(forms.ModelForm):

    class Meta:
        model = ConsumersCards
        fields = ['consumer_name', 'card_number', 'cod_card', 'expiration_date', 'flag_card']

class WhishesForm(forms.ModelForm):

    class Meta:
        model = Whishes
        fields = ['name_whishes_list', 'consumer', 'product', 'annotation', 'priority', 'amount']