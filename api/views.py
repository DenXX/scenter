""" Declares views for the API """

from django.db.models import Count, Q
from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status

from django.utils import timezone

from django.contrib.gis.geos import Polygon, Point

from api.models import *
from api.serializers import *
from api.utils import FencesFilter, ScentsFilter

import scenter.settings

class UserView(viewsets.ModelViewSet):
    """ View for the User model """

    lookup_field = 'username'       # Use username instead of pk
    queryset = ScenterUser.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return UserUpdateSerializer
        return UserSerializer


    def check_permissions(self, request):
        """ Check permissions, because we have difficult permissions for that """
        if request.method == 'GET':
            if not request.user.is_superuser:
                self.permission_denied(request)
        elif request.method in ('PUT', 'PATCH'):
            if 'username' not in request.DATA or request.user.username != request.DATA['username']:
                self.permission_denied(request)

class FenceListView(APIView):
    """ List fences available in the region """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        fences_queryset = FencesFilter.filter_inactive(Fence.objects.all()).area(field_name='_location')
        if 'ne' in self.request.QUERY_PARAMS:
            fences_queryset = FencesFilter.filter_no_scents(fences_queryset)
        # Check if bounding box is specified for filtering
        if 'bbox' in self.request.QUERY_PARAMS:
            fences_queryset = FencesFilter.filter_by_bbox(fences_queryset,
                self.request.QUERY_PARAMS['bbox'], settings.AREA_RATIO_FILTER_DEFAULT)
        # Check if a point location is specified for filtering
        if 'loc' in self.request.QUERY_PARAMS:
            accuracy = settings.DEFAULT_LOCATION_MATCH_ACCURACY
            if 'accuracy' in self.request.QUERY_PARAMS:
                accuracy = float(self.request.QUERY_PARAMS['accuracy'])
            fences_queryset = FencesFilter.filter_by_location(fences_queryset,
                self.request.QUERY_PARAMS['loc'], accuracy)
        # Create serializer for the list of fences
        fences_queryset = fences_queryset.extra(order_by=['-area'])
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
        """ Filter dead scents """
        return scents_queryset.filter(created__lt=timezone.now()).\
            filter(Q(due__gt=timezone.now()) | Q(due__isnull=True))


    def get(self, request):
        """ Returns a list of scents for a fence or for location """
        if 'fence_id' in request.QUERY_PARAMS:
            fence_id = request.QUERY_PARAMS['fence_id']
            scents_queryset = Scent.objects.filter(fence__id=fence_id)
            scents_queryset = self.filter_inactive(scents_queryset)
            first_scent_id = -1
            last_scent_id = -1
            if 'last_scent_id' in request.QUERY_PARAMS:
                last_scent_id = int(request.QUERY_PARAMS['last_scent_id'])
            if 'first_scent_id' in request.QUERY_PARAMS:
                first_scent_id = int(request.QUERY_PARAMS['first_scent_id'])
            scents_queryset = ScentsFilter.paginate(scents_queryset, settings.SCENTS_PAGE_SIZE,
                last_scent_id=last_scent_id, first_scent_id=first_scent_id)
            serializer = ScentSerializer(scents_queryset, many=True)
            return Response(serializer.data)

        if 'loc' in request.QUERY_PARAMS:
            location = request.QUERY_PARAMS['loc']
            fences = Fence.objects.all()
            accuracy = settings.DEFAULT_LOCATION_MATCH_ACCURACY
            if 'accuracy' in self.request.QUERY_PARAMS:
                accuracy = float(self.request.QUERY_PARAMS['accuracy'])
            fences = FencesFilter.filter_by_location(fences, location, accuracy)
            scents_queryset = Scent.objects.filter(fence__in=fences)
            scents_queryset = self.filter_inactive(scents_queryset)
            serializer = ScentSerializer(scents_queryset, many=True)
            return Response(serializer.data)
        # Otherwise raise 404
        raise Http404

    def post(self, request):
        """ Creates new scent for the given fence """
        # TODO: Check how to change value of serializer instead of this
        if 'fence_id' in request.QUERY_PARAMS:
            fence_id = request.QUERY_PARAMS['fence_id']
            # TODO: figure out why json gives mutable dict and form immutable
            data = request.DATA.copy()
            data.update({'fence': fence_id, 'author':request.user.username})
            serializer = ScentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors':'Fence is not specified'}, status=status.HTTP_400_BAD_REQUEST)


class ScentView(viewsets.ModelViewSet):
    """ View for a particular scent """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Scent.objects.all()
    serializer_class = ScentSerializer

class FeedbackView(APIView):
    """ View for users feedback """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = FeedbackSerializer

    def get(self, request):
        feedback_queryset = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # TODO: figure out why json gives mutable dict and form immutable
        data = request.DATA.copy()
        data.update({'author': request.user.id})
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
