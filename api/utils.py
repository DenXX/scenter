from datetime import datetime

from django.contrib.gis.geos import Polygon, Point
from django.contrib.gis.measure import Distance
from django.db.models import Q

from api.models import Fence, Scent


class FencesFilter:
    """ This class contains static methods for filtering fences """

    @staticmethod
    def filter_inactive(fences_queryset):
        """ Filters incative fences based on creation and due dates """
        return fences_queryset.filter(created__lt=datetime.now()).\
        	filter(Q(due__gt=datetime.now()) | Q(due__isnull=True))

    @staticmethod
    def filter_no_scents(fences_queryset):
        """ Filters fences without messages """
        fences_queryset = fences_queryset.annotate(num_scents=Count('scents'))
        return fences_queryset.filter(num_scents__gt=0)

    @staticmethod
    def filter_by_bbox(fences_queryset, bbox, area_ratio_filter=0):
        """ Filter fences query set by bounding box """
        bbox = bbox.split(',')
        # Check if we have 4 coordinates (top-left + botton-right)
        if len(bbox) != 4:
            raise Http404
        bbox = Polygon.from_bbox(map(float, bbox))
        # Do GIS within filter
        # TODO: How to do filtering by area without extra()?
        return fences_queryset.filter(_location__within=bbox).extra(
            where=['ST_Area("api_fence"."_location") >= %s'], params=[area_ratio_filter*bbox.area])

    @staticmethod
    def filter_by_location(fences_queryset, loc, accuracy):
        """ Filter fences query set by location """
        loc = loc.split(',')
        # Check if we have 4 coordinates (top-left + botton-right)
        if len(loc) != 2:
            raise Http404
        loc = Point(map(float, loc))
        return fences_queryset.filter(_location__distance_lte=(loc, Distance(m=accuracy)))


if __name__ == "__main__":
	print "Scenter API utility module"