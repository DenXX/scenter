
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon, Point, GEOSGeometry
from rest_framework.authtoken.models import Token

from scenter import settings

class Fence(models.Model):
    """ Represents a geo-fence (some shape) """

    # We are using GeoDjango, so need to replace manager
    objects = models.GeoManager()

    name = models.CharField(max_length=256, blank=False, help_text=u'The name '
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


class ScenterUser(AbstractUser):
    """ Stores information on user profile """

    def upload_to(instance, filename):
        return setting.MEDIA_ROOT + '%s/%s' % (instance.user.username, filename)

    userpic = models.ImageField(blank=True, null=True, upload_to=upload_to, help_text=u'Userpic')
    wormholes = models.ManyToManyField(Fence, related_name='wormhole_users',
        help_text=u'Wormhole allows a user to receive messages from a fence not in his current location')

    # Need this dirty trick, because otherwise to_native method of UserUpdateSerializer fails
    @property
    def password_confirm(self):
        return self.password

    class Meta:
        ordering = ('username',)

@receiver(post_save, sender=ScenterUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Scent(models.Model):
    """ Represents a message with a geo-fence associated with it """
    objects = models.GeoManager()

    # TODO: change this to a ForeignKey to User model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='scents',
        help_text=u'Author of the message')
    content = models.CharField(max_length=450, blank=False, help_text=u'Body '
        'of the message')
    created = models.DateTimeField(auto_now_add=True, db_index=True,
        help_text=u'When the message was created')
    due = models.DateTimeField(blank=True, null=True, db_index=True,
        help_text=u'When the message becomes inactive')
    fence = models.ForeignKey(Fence, help_text=u'Fence for the current message',
        related_name='scents')

    class Meta:
        ordering = ('-created',)
