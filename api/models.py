from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon, Point

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
        # TODO: Make it more general, not just circle
        self._location = Polygon(location)

    def get_location(self):
        return self._location

    location = property(get_location, set_location)


class ScentType(models.Model):
    """ Represents a type of the message """
    name = models.CharField(max_length=64, help_text=u'Type of the message')


class Scent(models.Model):
    """ Represents a message with a geo-fence associated with it """
    objects = models.GeoManager()

    # TODO: change this to a ForeignKey to User model
    author = models.CharField(max_length=40, blank=True, null=True, 
        help_text=u'Author of the message')
    type = models.ForeignKey(ScentType, help_text=u'The type of a message')
    title = models.CharField(max_length=40, blank=False, help_text=u'Title of '
        'the message')
    content = models.CharField(max_length=140, blank=False, help_text=u'Body '
        'of the message')
    created = models.DateTimeField(auto_now_add=True, db_index=True,
        help_text=u'When the message was created')
    due = models.DateTimeField(blank=True, null=True, db_index=True,
        help_text=u'When the message becomes inactive')
    fence = models.ForeignKey(Fence, help_text=u'Fence for the current message',
        related_name='scents')

    class Meta:
        ordering = ('created',)