""" Declares views for the API """

from django.db.models import Count
from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from datetime import datetime

from django.contrib.gis.geos import Polygon, Point

from api.models import Fence, Scent, Profile
from api.serializers import *
from api.utils import FencesFilter


class UserView(viewsets.ModelViewSet):
    """ View for the User model """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class FenceListView(APIView):
    """ List fences available in the region """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        fences_queryset = FencesFilter.filter_inactive(Fence.objects.all())
        if 'ne' in self.request.QUERY_PARAMS:
            fences_queryset = FencesFilter.filter_no_scents(fences_queryset)
        # Check if bounding box is specified for filtering
        if 'bbox' in self.request.QUERY_PARAMS:
            fences_queryset = FencesFilter.filter_by_bbox(fences_queryset,
                self.request.QUERY_PARAMS['bbox'])
        # Check if a point location is specified for filtering
        if 'loc' in self.request.QUERY_PARAMS:
            fences_queryset = FencesFilter.filter_by_location(fences_queryset,
                self.request.QUERY_PARAMS['loc'])
        # Create serializer for the list of fences
        serializer = FenceSerializer(fences_queryset, many=True)
        return Response(serializer.data)


    def post(self, request):
        """ Creates a new fence """
        serializer = FenceSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FenceView(viewsets.ModelViewSet):
    """ View for a particular fence """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Fence.objects.all()
    serializer_class = FenceSerializer


class ScentListView(APIView):
    """ View for a list of scents """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def filter_inactive(self, scents_queryset):
        return scents_queryset.filter(created__lt=datetime.now(),
            due__gt=datetime.now())


    def get(self, request, fence_id):
        """ Returns a list of scents for a fence or for location """
        if 'fence_id' in request.QUERY_PARAMS:
            fence_id = request.QUERY_PARAMS['fence_id']
            scents_queryset = Scent.objects.filter(fence__id=fence_id)
            scents_queryset = self.filter_inactive(scents_queryset)
            serializer = ScentSerializer(scents_queryset)
            return Response(serializer.data)

        if 'loc' in request.QUERY_PARAMS:
            location = request.QUERY_PARAMS['loc']
            fences = Fence.objects.all()
            fences = FencesFilter.filter_by_location(fences, location)
            scents = Scent.objects.filter(fence__in=fences)
            scents = scents.extra(order_by=['-created'])
            serializer = ScentSerializer(scents, many=True)
            return Response(serializer.data)
        # Otherwise raise 404
        raise Http404


    def post(self, request, fence_id):
        """ Creates new scent for the given fence """
        # TODO: Check how to change value of serializer instead of this
        serializer = ScentSerializer(data=request.DATA,
            context={'fence': fence_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScentView(viewsets.ModelViewSet):
    """ View for a particular scent """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Scent.objects.all()
    serializer_class = ScentSerializer
