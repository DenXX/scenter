from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from api import views

admin.autodiscover()

router = DefaultRouter()
router.register(r'scent', views.ScentView)
router.register(r'fence', views.FenceView)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # API urls
    url(r'^fences/$', views.FenceListView.as_view(), name='fences_view'),
    url(r'^scents/(?P<fence_id>[0-9]+)', views.ScentListView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
