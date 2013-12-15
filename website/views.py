from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView

from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

from api.models import ScenterUser
from website.forms import UserProfileForm

class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail


class UserProfileView(UpdateView):
    """ User profile view """
    model = ScenterUser
    fields = ['first_name', 'last_name', 'userpic']

    def get_form_class(self):
        return UserProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')
