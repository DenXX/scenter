""" Declares views for the API """

from django.db.models import Count
from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from django.contrib.gis.geos import Polygon, Point

from api.models import Fence, Scent
from api.serializers import FenceSerializer, ScentSerializer

class FencesFilter:
    """ This class contains static methods for filtering fences """

    @staticmethod
    def filter_inactive(fences_queryset):
        """ Filters incative fences based on creation and due dates """
        return fences_queryset.filter(created__lt=datetime.now(),
            due__gt=datetime.now())

    @staticmethod
    def filter_no_scents(fences_queryset):
        """ Filters fences without messages """
        fences_queryset = fences_queryset.annotate(num_scents=Count('scents'))
        return fences_queryset.filter(num_scents__gt=0)

    @staticmethod
    def filter_by_bbox(fences_queryset, bbox):
        """ Filter fences query set by bounding box """
        bbox = bbox.split(',')
        # Check if we have 4 coordinates (top-left + botton-right)
        if len(bbox) != 4:
            raise Http404
        bbox = Polygon.from_bbox(map(float, bbox))
        # Do GIS within filter
        # TODO: for some reason overlaps filter doesn't work, but fits better
        return fences_queryset.filter(_location__within=bbox)

    @staticmethod
    def filter_by_location(fences_queryset, loc):
        """ Filter fences query set by location """
        loc = loc.split(',')
        # Check if we have 4 coordinates (top-left + botton-right)
        if len(loc) != 2:
            raise Http404
        loc = Point(map(float, loc))
        # Do GIS bounding box overlaps filter
        return fences_queryset.filter(_location__contains=loc)


class FenceListView(APIView):
    """ List fences available in the region """

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
    queryset = Fence.objects.all()
    serializer_class = FenceSerializer

class ScentListView(APIView):
    """ View for a list of scents """

    def filter_inactive(self, scents_queryset):
        return scents_queryset.filter(created__lt=datetime.now(),
            due__gt=datetime.now())


    def get(self, request, fence_id):
        """ Returns a list of scents for a fence """
        scents_queryset = Scent.objects.filter(fence__id=fence_id)
        scents_queryset = self.filter_inactive(scents_queryset)
        serializer = ScentSerializer(scents_queryset)
        return Response(serializer.data)


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
    queryset = Scent.objects.all()
    serializer_class = ScentSerializer


class ScentsLocationView(APIView):
    """ Returns all scents for a location """

    def get(self, request):
        if 'loc' not in request.QUERY_PARAMS:
            raise Http404

        location = request.QUERY_PARAMS['loc']
        fences = Fence.objects.all()
        fences = FencesFilter.filter_by_location(fences, location)
        scents = Scent.objects.filter(fence__in=fences)
        scents = scents.extra(order_by=['-created'])
        serializer = ScentSerializer(scents, many=True)
        return Response(serializer.data)