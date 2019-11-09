from django import forms


class DateForm(forms.Form):
    date = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({
            'class': 'form-control',
            "name": "date"})


class BookForm(forms.Form):

    CHOICES = [(['B-101', '10:00'], 'B-101'), (['B-201', '10:00'], 'B-201')]
    choice_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['choice_field'].widget.attrs.update({})
