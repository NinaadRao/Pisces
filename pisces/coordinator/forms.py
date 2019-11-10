from django import forms


class DateForm(forms.Form):
    date = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({})


class BookForm(forms.Form):
    chosen_labs_field = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        print(self.fields)
        self.fields['chosen_labs_field'].widget.attrs.update({'id': "csn_labs_field"})
