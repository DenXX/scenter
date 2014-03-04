from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, CreateView

from website.views import RegistrationViewUniqueEmail, UserProfileView

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^scenter/$', 'website.views.home'),
    url(r'^main/$', TemplateView.as_view(template_name="main.html"), name='main'),
    url(r'^about$', TemplateView.as_view(template_name="about.html"),
        name='about'),
    url(r'^$', TemplateView.as_view(template_name="tutorial.html"), name='tutorial'),
    url(r'^admin/', include(admin.site.urls)),

    # Authentication urls
    # Registration urls
    url(r'account/', include('registration.backends.default.urls')),
    url(r'^account/register', RegistrationViewUniqueEmail.as_view(),
                        name='registration_register'),
    url(r'^profile/', UserProfileView.as_view(
        template_name='registration/profile.html'),
        name='profile'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
