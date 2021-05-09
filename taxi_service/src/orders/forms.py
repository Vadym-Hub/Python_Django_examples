from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Форма заказа.
    """
    name = forms.RegexField(
        label='Имя заказчика',
        regex=r'[а-яА-ЯёЁ]',
        error_messages={'invalid': 'Пожалуйста введите имя кириллицей'}
    )
    phone = forms.RegexField(
        label='Ваш телефон',
        regex=r'[+380][(][0-9]{2}[)][0-9]{3}[-][0-9]{2}[-][0-9]{2}',
        error_messages={'invalid': 'Пожалуйста введите телефон в формате +380(xx)xxx-xx-xx'},
        widget=forms.TextInput(attrs={'placeholder': '+380(XX)XXX-XX-XX'})
    )
    desired_time = forms.TimeField(
        label='Желаемое время подачи авто ',
        widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'XX:XX'}))

    class Meta(object):
        model = Order
        fields = (
            'name',
            'phone',
            'address_from',
            'destination',
            'desired_time',
        )
