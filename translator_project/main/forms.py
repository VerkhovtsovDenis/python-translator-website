from django import forms
from main.models import SupportLanguage


class TranslateForm(forms.Form):
    input_code = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control prettyprint',
            'rows': 15,
            'placeholder': 'Введите ваш код на Pascal...'
        }),
        label=''
    )

    language = forms.CharField(
        widget=forms.HiddenInput(),
        initial='python'
    )
