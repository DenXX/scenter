from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon, Point, GEOSGeometry

import scenter.settings

class Profile(models.Model):
    """ Stores information on user profile """

    def upload_to(instance, filename):
        return setting.MEDIA_ROOT + '%s/%s' % (instance.user.username, filename)

    user = models.OneToOneField(User, primary_key=True, related_name='profile',
        help_text=u'Profile for the given user')
    userpic = models.ImageField(upload_to=upload_to, help_text=u'Userpic')
    sniffing = models.ManyToManyField(User, related_name='sniffers',
        help_text=u'A list of users the current users follows/sniffs')


class Fence(models.Model):
    """ Represents a geo-fence (some shape) """

    # We are using GeoDjango, so need to replace manager
    objects = models.GeoManager()

    name = models.CharField(max_length=128, blank=False, help_text=u'The name '
        'of the fence')
    created = models.DateTimeField(auto_now_add=True, help_text=u'When the '
        'fence was created')
    due = models.DateTimeField(blank=True, null=True, help_text=u'When the '
        'fence will become inactive')
    _location = models.PolygonField(help_text=u'Polygon region of the fence')

    # Create methods to convert location representations from numbers to GEOMETRY
    def set_location(self, location):
        self._location = GEOSGeometry(location)

    def get_location(self):
        return self._location.json

    location = property(get_location, set_location)


class Scent(models.Model):
    """ Represents a message with a geo-fence associated with it """
    objects = models.GeoManager()

    # TODO: change this to a ForeignKey to User model
    author = models.ForeignKey(User, related_name='scents',
        help_text=u'Author of the message')
    content = models.CharField(max_length=140, blank=False, help_text=u'Body '
        'of the message')
    created = models.DateTimeField(auto_now_add=True, db_index=True,
        help_text=u'When the message was created')
    due = models.DateTimeField(blank=True, null=True, db_index=True,
        help_text=u'When the message becomes inactive')
    fence = models.ForeignKey(Fence, help_text=u'Fence for the current message',
        related_name='scents')

    class Meta:
        ordering = ('-created',)
