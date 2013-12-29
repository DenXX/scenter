from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Website urls
    url(r'^', include('website.urls')),

    # API urls
    url(r'^api/', include('api.urls')),

    # Token authentication request token url
    url(r'^api-token-auth$', 'rest_framework.authtoken.views.obtain_auth_token'),

    # Examples:
    # url(r'^$', 'scenter.views.home', name='home'),
    # url(r'^scenter/', include('scenter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
