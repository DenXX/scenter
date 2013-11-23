""" Declares views for the API """

from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.gis.geos import Polygon, Point

from api.models import Fence, Scent
from api.serializers import FenceSerializer, ScentSerializer


class FenceListView(APIView):
    """ List fences available in the region """

    def filter_by_bbox(self, fences_queryset, bbox):
        """ Filter fences query set by bounding box """
        bbox = bbox.split(',')
        # Check if we have 4 coordinates (top-left + botton-right)
        if len(bbox) != 4:
            raise Http404
        bbox = Polygon.from_bbox(map(float, bbox))
        # Do GIS bounding box overlaps filter
        return fences_queryset.filter(location__bboverlaps=bbox)


    def filter_by_location(self, fences_queryset, loc):
        """ Filter fences query set by location """
        loc = loc.split(',')
        # Check if we have 4 coordinates (top-left + botton-right)
        if len(loc) != 2:
            raise Http404
        loc = Point(map(float, loc))
        # Do GIS bounding box overlaps filter
        return fences_queryset.filter(location__contains=loc)


    def get(self, request):
        fences_queryset = Fence.objects.all()
        # Check if bounding box is specified for filtering
        if 'bbox' in self.request.QUERY_PARAMS:
            fences_queryset = self.filter_by_bbox(fences_queryset,
                self.request.QUERY_PARAMS['bbox'])

        # Check if a point location is specified for filtering
        if 'loc' in self.request.QUERY_PARAMS:
            fences_queryset = self.filter_by_location(fences_queryset,
                self.request.QUERY_PARAMS['loc'])
        # Create serializer for the list of fences
        serializer = FenceSerializer(fences_queryset, many=True)
        return Response(serializer.data)
