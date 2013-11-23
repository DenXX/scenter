""" Declares views for the API """

from rest_framework import viewsets

from api.models import Fence, Scent
from api.serializers import FenceSerializer, ScentSerializer


class FenceViewSet(viewsets.ModelViewSet):
    """ API endpoint that can be used to view and edit fences """
    queryset = Fence.objects.all()
    serializer_class = FenceSerializer


class ScentViewSet(viewsets.ModelViewSet):
    """ API endpoint that can be used to view and edit messages """
    queryset = Scent.objects.all()
    serializer_class = ScentSerializer