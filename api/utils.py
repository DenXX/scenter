from django.utils import timezone

from django.contrib.gis.geos import Polygon, Point
from django.contrib.gis.measure import Distance
from django.db.models import Q

from api.models import Fence, Scent


class FencesFilter:
    """ This class contains static methods for filtering fences """

    @staticmethod
    def filter_inactive(fences_queryset):
        """ Filters incative fences based on creation and due dates """
        return fences_queryset.filter(created__lt=timezone.now()).\
        	filter(Q(due__gt=timezone.now()) | Q(due__isnull=True))

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

class ScentsFilter:
    """ This class contains static methods for filtering scents """

    @staticmethod
    def paginate(queryset, limit, first_scent_id=-1, last_scent_id=-1):
        if first_scent_id != -1:
            # Get a page of scents starting from last_id scent
            return queryset.order_by('-created').filter(id__gt=first_scent_id)
        elif last_scent_id != -1:
            # Get a page of scents starting from last_id scent
            return queryset.order_by('-created').filter(id__lt=last_scent_id)[:limit]
        else:
            return queryset.order_by('-created')[:limit]

if __name__ == "__main__":
	print "Scenter API utility module"
