from django import forms


class PascalCodeForm(forms.Form):
    pascal_code = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control prettyprint",
            'rows': "15",
            "placeholder": "Введите ваш код на Pascal..."}),
        label='',
        max_length=5000)
