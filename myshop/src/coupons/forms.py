from django import forms


class CouponApplyForm(forms.Form):
    """Форма для предоставления пользователям возможности ввести код купона."""
    code = forms.CharField()
