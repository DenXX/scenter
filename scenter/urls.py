from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^scenter/$', 'website.views.home'),
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    url(r'^about$', TemplateView.as_view(template_name="about.html")),
    url(r'^1$', TemplateView.as_view(template_name="base_copy.html")),
    url(r'^admin/', include(admin.site.urls)),

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
