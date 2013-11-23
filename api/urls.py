from django.conf.urls import patterns, include, url
from django.contrib import admin

from api import views

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # API urls
    url(r'^fences/$', views.FenceListView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
