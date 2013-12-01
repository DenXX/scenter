function deleteMessages(mid){
        $.ajax({
        // TODO: need to use url Django tag?
        url: 'api/scent/' + mid + '/',
        cache: false,
        type: 'DELETE',
                dataType: "json",
                success: function(data){
                        console.log('deleted');
                },
                error: function(){
                        console.log('error delete');
                }
        });
}
function convertPolygonForApi(polygon_coords) {
    // Add start point to the polygon to close it
    polygon_coords.push(polygon_coords[0]);
    res = '{ \"type\": \"Polygon\", \"coordinates\": [ [';
    res += polygon_coords;
    res = res + '] ] }';
    return res.replace(/\(/g,'[').replace(/\)/g,']')
}

function populateMessages(fencePolygon){
        $.ajax({
        // TODO: need to use url Django tag?
        url: 'api/scents/' + fencePolygon.id + '/',
        cache: false,
        type: 'GET',
                dataType: "json",
                success: function(data){
                        messagelist = data;

			if (messagelist.length > 0) {
                        	$('#messagelist').html("");
                        
                        	$.each(messagelist, function(index, message) {
                        	        elementid = appendMessage(messagelist[index].content);
					var m = document.getElementById(elementid);
					m.setAttribute("mid", messagelist[index].id);
                        	});
			}
			else
				$('#messagelist').html("Nothing is scenting here.");
                },
                error: function(){
                        $('#messagelist').html("Nothing is scenting here.");
                }
        });
}


function postMessage(fencePolygon, text, eid) {
    scent = null;
    var due = new Date();
    due.setDate(due.getDate() + 2);

    $.ajax({
        url: 'api/scents/' + fencePolygon.id + '/',
        cache: false,
        type: 'POST',
        data:  {"author": "Ghost", "type": "1", "title": "Scent title", "content": text,
               "due": due.toISOString(), "fence": fencePolygon.id},
        dataType: "json",
        success: function(data){
            var me = document.getElementById(eid);
	    me.setAttribute("mid", data.id);
	    console.log(data.id);
        },
        error: function(){
            alert("Something happened here... Not sure what, but it failed. :( Sorry");
        }
    });
    return -1;
}

function getPolygonOptions(active) {
    if (active)
        return {strokeColor: 'green',
                strokeOpacity: 1.0,
                strokeWeight: 3,
                fillColor: 'green',
                fillOpacity: 0.5};
    else
        return { strokeColor: 'green',
                 strokeOpacity: 0.8,
                 strokeWeight: 1,
                 fillColor: 'green',
                 fillOpacity: 0.1};
}

function selectFence(fence) {
    if (currentPolygon) {
        currentPolygon.setOptions(getPolygonOptions(false));
    }

    populateMessages(fence);
    currentPolygon = fence;
    currentPolygon.setOptions(getPolygonOptions(true));
}

// TODO: If we move map and fence goes out of scope, we should remove window.
function showInfoWindow(fence, coords) {
  var contentString = '<div>' + fence.name + '</div>';
  if (infoWindow)
    infoWindow.close();
  infoWindow = new google.maps.InfoWindow({
      position: coords,
      content: contentString
  });
  infoWindow.open(map);
}

function displayFence(fence) {
    if (fence.id in polygons)
        return;
    // Define the LatLng coordinates for the polygon's path.
    var vertices = new Array();
    var fence_location = JSON.parse(fence.location);
    for (var i = 0; i < fence_location.coordinates[0].length; ++i) {
        vertices.push(new google.maps.LatLng(fence_location.coordinates[0][i][0],
            fence_location.coordinates[0][i][1]));
    }
    fence_polygon = new google.maps.Polygon({paths: vertices});
    fence_polygon.setOptions(getPolygonOptions(false));
    fence_polygon.id = fence.id;
    fence_polygon.name = fence.name;

    google.maps.event.addListener(fence_polygon, 'click', function(event){
        selectFence(this);
        showInfoWindow(this, event.latLng);
    });
    fence_polygon.setMap(map);
    polygons[fence_polygon.id] = fence_polygon;
}

function hideInvisibleFences(boundingBox) {
    for (var id in polygons) {
        path = polygons[id].getPath();
        for (var i = 0; i < path.getLength(); ++i) {
            if (!boundingBox.contains(path.getAt(i))) {
                polygons[id].setMap(null);
                delete polygons[id];
                break;
            }
        }
    }
}

function updateFences(boundingBox) {
    hideInvisibleFences(boundingBox);

    var bbox = boundingBox.getNorthEast().lat()+','+boundingBox.getNorthEast().lng()+
        ','+boundingBox.getSouthWest().lat()+','+boundingBox.getSouthWest().lng();
    $.ajax({
        url: 'api/fences/?bbox=' + bbox,
        cache: false,
        type: 'GET',
        dataType: "json",
        success: function(data){
            data.forEach(displayFence);
        },
        error: function(){
            alert("Something happened here... Not sure what, but it failed. :( Sorry");
        }
    });
}
