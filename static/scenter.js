
function convertPolygonForApi(polygon_coords) {
    // Add start point to the polygon to close it
    polygon_coords.push(polygon_coords[0]);
    res = '{ \"type\": \"Polygon\", \"coordinates\": [ [';
    res += polygon_coords;
    res = res + '] ] }';
    return res.replace(/\(/g,'[').replace(/\)/g,']')
}