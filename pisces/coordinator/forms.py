from django import forms


class DateForm(forms.Form):
    date = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({
            'class': 'form-control',
            "name": "date"})
