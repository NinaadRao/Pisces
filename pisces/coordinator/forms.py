from django import forms


class UsersLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, )

    def __init__(self, *args, **kwargs):
        super(UsersLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name": "username"})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            "name": "password"})

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        return super(UsersLoginForm, self).clean(*args, **keyargs)


class DateForm(forms.Form):
    date = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({})


class BookForm(forms.Form):
    chosen_labs_field = forms.CharField(widget=forms.HiddenInput())
    chosen_company_visit_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        print(self.fields)
        self.fields['chosen_labs_field'].widget.attrs.update({'id': "csn_labs_field"})
        self.fields['chosen_company_visit_id'].widget.attrs.update({'id': "csn_company_visit_id_field"})
