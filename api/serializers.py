""" This file declares some serializes for RESTful API model serialization """

from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from rest_framework import pagination, serializers

from api.models import *

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user with a profile """
    # TODO: username should be read-only, but then we cannot specify it
    # on POST

    class Meta:
        model = ScenterUser
        fields = ('username', 'email', 'first_name', 'last_name', 'userpic', 'wormholes')
        read_only_fields = ('username',)


class UserUpdateSerializer(UserSerializer):
    """ Serializer for creating or updating a user """
    password = serializers.CharField(max_length=128, min_length=4)
    password_confirm = serializers.CharField(max_length=128, min_length=4)

    def validate(self, attrs):
        """ Validates that password and password_confirm are the same """

        if 'password' in attrs:
            if 'password_confirm' not in attrs:
                raise serializers.ValidationError("password_confirm field is required")
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError("Passwords don't match")

        # Check uniqueness of username and password
        if getattr(self, 'object', None) == None: # Check if this is PUT or POST
            if ScenterUser.objects.filter(username=attrs['username']).count() > 0:
                raise serializers.ValidationError("A user with the given name already exists.")
            if ScenterUser.objects.filter(email=attrs['email']).count() > 0:
                raise serializers.ValidationError("A user with the given email already exists.")
        return attrs

    def restore_object(self, attrs, instance):
        """ restore_objects needs special treatmeant for users """
        if instance == None:
            # Check if such user already exists
            # if ScenterUser.objects.filter(username=attrs['username']).count() > 0:
            #     raise serializers.ValidationError("User with this username already exists")

            instance = ScenterUser.objects.create_user(username=attrs['username'],
                password=attrs['password'])
            del attrs['password_confirm']
            del attrs['password']
        else:
            if 'password' in attrs:
                instance.set_password(attrs['password'])
                del attrs['password_confirm']
                del attrs['password']
        return super(UserUpdateSerializer, self).restore_object(attrs, instance)

    def save_object(self, obj, **kwargs):
        if 'force_insert' in kwargs:
            del kwargs['force_insert']
        obj.save(**kwargs)

    def to_native(self, obj):
        res = super(UserUpdateSerializer, self).to_native(obj)
        del res['password']
        del res['password_confirm']
        # TODO: Probably there is a better way...
        res.fields['password']._value = ''
        res.fields['password_confirm']._value = ''
        return res

    class Meta:
        model = ScenterUser
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name', 'userpic',
            'wormholes')


class ScentSerializer(serializers.ModelSerializer):
    """ Serializer for Scent model """
    author = serializers.SlugRelatedField(slug_field='username')

    class Meta:
        model = Scent
        fields = ('id', 'author', 'content', 'created', 'due', 'fence')

class PaginatedScentSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of scent querysets.
    """
    class Meta:
        object_serializer_class = ScentSerializer

# TODO: HyperlinkedModelSerializers are better
class FenceSerializer(serializers.ModelSerializer):
    """ Serializer for Fence model """
    location = serializers.CharField(source='location')
    scents = serializers.SerializerMethodField('paginated_scents')
    # TODO: Why is this commented out?
    # due = serializers.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p',])

    def paginated_scents(self, fence):
        paginator = Paginator(fence.scents.all(), settings.SCENTS_PAGE_SIZE)
        scents = paginator.page(1)
        serializer = PaginatedScentSerializer(scents)
        return serializer.data

    class Meta:
        model = Fence
        fields = ('id', 'name', 'created', 'due', 'location', 'scents')

class FeedbackSerializer(serializers.ModelSerializer):
    """ Serializer for Scent model """

    class Meta:
        model = Feedback
        fields = ('author', 'text')
