"""
    This script loads polygons from OpenStreetMap json format into database of fences.
"""

import json
import os
import string
import sys

from random import choice

_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scenter.settings")

from api.models import Fence

def get_geo_django_polygon(coordinates):
    res = 'POLYGON(('

    for index, point in enumerate(coordinates):
        if index > 0:
            res += ','
        res += str(point[0]) + ' ' + str(point[1])
    return res + '))'

def main(input_filename):
    with open(input_filename, 'r') as input:
        for counter, line in enumerate(input):
            building = json.loads(line, encoding='utf8')
            if len(building['name']) > 0:
                polygon = get_geo_django_polygon(building['points'])
                id = building['name'].replace(' ','_').lower()
                if Fence.objects.filter(id=id).exists():
                    id += ''.join(choice(string.ascii_uppercase + string.digits) for x in range(10))
                Fence.objects.create(id=id, name=building['name'], location=polygon)
            print counter

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python load_polygons.py <input_file.json>'
        exit()
    main(sys.argv[1])