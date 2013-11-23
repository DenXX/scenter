""" This file declares some serializes for RESTful API model serialization """

from rest_framework import serializers

from api.models import Fence, Scent

class FenceSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for Fence model """
    class Meta:
        model = Fence
        fields = ('id', 'name', 'created', 'due', '_location')


class ScentSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for Scent model """
    class Meta:
        model = Scent
        fields = ('id', 'author', 'type', 'title', 'content', 'created', 'due',
            'fence')
