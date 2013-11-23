""" This file declares some serializes for RESTful API model serialization """

from rest_framework import serializers

from api.models import Fence, Scent

# TODO: HyperlinkedModelSerializers are better
class FenceSerializer(serializers.ModelSerializer):
    """ Serializer for Fence model """
    location = serializers.CharField(source='location')
    due = serializers.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p',])
    class Meta:
        model = Fence
        fields = ('id', 'name', 'created', 'due', 'location')


class ScentSerializer(serializers.ModelSerializer):
    """ Serializer for Scent model """
    class Meta:
        model = Scent
        fields = ('id', 'author', 'type', 'title', 'content', 'created', 'due',
            'fence')
