from django import forms

from api.models import ScenterUser

class AccountCreationForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        super(AccountCreationForm, self).clean()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Passwords don\'t match')

    class Meta:
        model = ScenterUser
        fields = ('username', 'email', 'password', 'password_confirm')
