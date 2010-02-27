from django import forms
from common.models import User


class UserForm(forms.ModelForm):
    first_name=forms.CharField(max_length=User._meta.get_field('first_name').max_length, \
                               required=True)
    
    class Meta:
        model = User
        fields = ('contacts', 'email', 'biography', 'birthdate', 'last_name',
                  'first_name')
