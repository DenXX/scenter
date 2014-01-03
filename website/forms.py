
from django.forms import ModelForm
from api.models import ScenterUser


class UserProfileForm(ModelForm):
    """ A form to update user profile information """
    class Meta:
        model = ScenterUser
        fields = ['first_name', 'last_name', 'userpic']
