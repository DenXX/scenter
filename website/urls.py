from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, CreateView

from website.views import RegistrationViewUniqueEmail

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^scenter/$', 'website.views.home'),
    url(r'^$', TemplateView.as_view(template_name="main.html")),
    url(r'^about$', TemplateView.as_view(template_name="about.html"),
        name='about'),
    url(r'^admin/', include(admin.site.urls)),

    # Authentication urls
    # Registration urls
    url(r'account/', include('registration.backends.default.urls')),
    url(r'^account/register', RegistrationViewUniqueEmail.as_view(),
                        name='registration_register'),
    url(r'^profile', TemplateView.as_view(
        template_name='users/profile.html'),
        name='profile'),


    # Examples:
    # url(r'^$', 'scenter.views.home', name='home'),
    # url(r'^scenter/', include('scenter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
