""" This file declares some serializes for RESTful API model serialization """

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models import *

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user with a profile """
    # username = serializers.CharField(source='user.username')
    # email = serializers.CharField(source='user.email')

    class Meta:
        model = User
        fields = ('username', 'email')


class UserUpdateSerializer(UserSerializer):
    """ Serializer for creating or updating a user """
    password = serializers.CharField(required=True, max_length=128, min_length=4)
    password_confirm = serializers.CharField(required=True, max_length=128, min_length=4)

    def validate(self, attrs):
        """ Validates that password and password_confirm are the same """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def restore_object(self, attrs, instance=None):
        """ restore_objects needs special treatmeant for users """
        if instance == None:
            instance = User.objects.create_user(username=attrs['username'],
                email=attrs['email'], password=attrs['password'])
        else:
            instance.set_password(attrs['password'])
        del attrs['password_confirm']
        del attrs['password']
        return super(UserSerializer, self).restore_object(attrs, instance)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')


# TODO: HyperlinkedModelSerializers are better
class FenceSerializer(serializers.ModelSerializer):
    """ Serializer for Fence model """
    location = serializers.CharField(source='location')
    # due = serializers.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p',])
    class Meta:
        model = Fence
        fields = ('id', 'name', 'created', 'due', 'location')


class ScentSerializer(serializers.ModelSerializer):
    """ Serializer for Scent model """
    class Meta:
        model = Scent
        fields = ('id', 'author', 'content', 'created', 'due', 'fence')
