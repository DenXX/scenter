from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, CreateView

from website.forms import AccountCreationForm

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
    url(r'^login', 'django.contrib.auth.views.login',
        {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^signup', CreateView.as_view(
            template_name='users/signup.html',
            form_class=AccountCreationForm,
            success_url='/'),
        name='signup'),
    url(r'^profile', TemplateView.as_view(
        template_name='users/profile.html'),
        name='profile'),

    # API urls
    url(r'^api/', include('api.urls')),

    # Examples:
    # url(r'^$', 'scenter.views.home', name='home'),
    # url(r'^scenter/', include('scenter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
