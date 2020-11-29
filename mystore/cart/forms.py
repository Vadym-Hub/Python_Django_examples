from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]


class CartAddProductForm(forms.Form):
    """Форма додавання продуктів в кошик"""
    quantity = forms.TypedChoiceField(label='Кількість:',
                                      choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
