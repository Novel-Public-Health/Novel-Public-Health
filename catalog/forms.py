from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class RenewMovieForm(forms.Form):
    """Form for a librarian to renew movies."""
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Contact

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    # def __init__(self, *args, **kwargs):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class NameWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        super().__init__(
            [forms.TextInput(), 
            forms.TextInput()],
            attrs
        )
    def decompress(self, value):
        if value:
            return value.split('')
        return ['', '']


class NameField(forms.MultiValueField):
    widget = NameWidget
    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(),
            forms.CharField()
        )

        super().__init__(fields, *args, **kwargs)
    
    def compress(self, data_list):
        return f'{data_list[0]} {data_list[1]}'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'body'
        ]

    name = NameField()
    email = forms.EmailField(label='E-mail')
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'name',
            'email',
            'subject',
            'body',
            Submit('submit', 'Submit', css_class='myButton')

        )