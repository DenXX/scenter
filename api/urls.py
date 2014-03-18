from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from api import views

admin.autodiscover()

router = DefaultRouter()
router.register(r'user', views.UserView)
router.register(r'scent', views.ScentView)
router.register(r'fence', views.FenceView)
router.register(r'feedback', views.FeedbackView)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # API urls
    url(r'^fences/$', views.FenceListView.as_view(), name='fences_view'),
    url(r'^scents/', views.ScentListView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
