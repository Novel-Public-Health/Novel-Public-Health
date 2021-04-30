from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # For checking renewal date range.

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Contact

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

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

# On the profile page, change a user's username and email account info.
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']       