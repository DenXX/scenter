
var scenterControllers = angular.module('scenterControllers', []);

scenterControllers.controller('FenceCtrl', ['$scope', '$http', '$cookies', 'Fences', function ($scope, $http, $cookies, Fences) {
    var mapOptions = {
        zoom: 15,
        center: new google.maps.LatLng(33.7920235, -84.325642),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false
    };

    $scope.map = new google.maps.Map($('#map-canvas').get(0), mapOptions);
    $scope.fences = {};
    $scope.current_polygon = null;
    $scope.infoWindow = null;
    // Info about polygon just created
    $scope.newPolygonName = null;
    $scope.createdPolygon = null

    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: null,
        drawingControl: true,
        drawingControlOptions: {
          position: google.maps.ControlPosition.TOP_CENTER,
          size: 20,
          drawingModes: [
            google.maps.drawing.OverlayType.POLYGON
          ]
        },
    });
    drawingManager.setMap($scope.map);



    getPolygonOptions = function (active) {
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
    };

    selectFence = function (fence) {
        if ($scope.currentFence) {
            $scope.currentFence.setOptions(getPolygonOptions(false));
        }

        $scope.currentFence = fence;
        $scope.currentFence.setOptions(getPolygonOptions(true));
        $scope.$digest();
    };

    deselectCurrentFence = function() {
        if ($scope.currentFence != null) {
            $scope.currentFence.setOptions(getPolygonOptions(false));
            $scope.currentFence = null;
        }
        if ($scope.infoWindow != null)
            $scope.infoWindow.close();
        $scope.$digest();
    };

    // TODO: If we move map and fence goes out of scope, we should remove window.
    showInfoWindow = function (fence, coords) {
        var contentString = '<div>' + fence.name + '</div>';
        if ($scope.infoWindow)
            $scope.infoWindow.close();
        $scope.infoWindow = new google.maps.InfoWindow({
            position: coords,
            content: contentString
        });
        $scope.infoWindow.open($scope.map);
    };

    convertPolygonForApi = function (polygon_coords) {
        // Add start point to the polygon to close it
        polygon_coords.push(polygon_coords[0]);
        res = '{ \"type\": \"Polygon\", \"coordinates\": [ [';
        res += polygon_coords;
        res = res + '] ] }';
        return res.replace(/\(/g,'[').replace(/\)/g,']')
    }

    // TODO: Create service for all this functions
    displayFence = function (fence) {
        if (fence.id in $scope.fences)
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

        fence_polygon.setMap($scope.map);
        $scope.fences[fence_polygon.id] = fence_polygon;
    };

    hideInvisibleFences = function (fences) {
        // Create hashset of ids in returned set
        ids_to_keep = {};
        for (var i = 0; i < fences.length; ++i)
            ids_to_keep[fences[i].id] = true;

        // Delete items not in this list
        for (var id in $scope.fences) {
            // If not in the list to keep or it is not current (if there is current)
            if (!(id in ids_to_keep) && 
                ($scope.currentFence == null || $scope.currentFence.id != id)) {
                $scope.fences[id].setMap(null);
                delete $scope.fences[id];
            }
        }
    }

    $scope.updateFences = function() {
        var boundingBox = $scope.map.getBounds();
        var map_bbox = boundingBox.getNorthEast().lat()+','+boundingBox.getNorthEast().lng()+
            ','+boundingBox.getSouthWest().lat()+','+boundingBox.getSouthWest().lng();
        Fences.query({bbox: map_bbox}, function(fences){
            hideInvisibleFences(fences);
            fences.forEach(displayFence);
        });
    };

    $scope.resetSaveFence = function() {
        $scope.createdPolygon.setMap(null);
        $scope.newPolygonName = null;
        $scope.createdPolygon = null;
        $('#saveFenceDialog').modal('toggle');
    }

    $scope.saveFence = function() {
        var data = {location:convertPolygonForApi($scope.createdPolygon.getPath().getArray()),
            name:$scope.newPolygonName};
        // TODO: do this with Angular service
        $http({method:'POST', url: '/api/fences/', data: data,
            headers: {'X-CSRFToken':$cookies.csrftoken}}).
          success(function(data, status, headers, config) {
            $scope.updateFences();
          }).
          error(function(data, status, headers, config) {
            // TODO: I guess we don't show this to the user, but email?
            alert(data.errors);
          });

        $scope.resetSaveFence();
    }

    // TODO: How to skip this in not admin view?
    google.maps.event.addListener(drawingManager, 'polygoncomplete', function(polygon) {
        // Set event handler for click
        // google.maps.event.addListener(polygon, 'click', function(event){
            // selectFence(this);
            // showInfoWindow(this, event.latLng);
        // });
        $scope.createdPolygon = polygon;
        $('#saveFenceDialog').modal('toggle');
    });

    google.maps.event.addListenerOnce($scope.map, 'tilesloaded', function () {
        $scope.updateFences();
    });
    google.maps.event.addListener($scope.map, 'dragend', function () {
        $scope.updateFences();
    });
    google.maps.event.addListener($scope.map, 'zoom_changed', function () {
        $scope.updateFences();
    });
    google.maps.event.addListener($scope.map, 'click', function(){
        deselectCurrentFence();
    });
}]);
 
scenterControllers.controller('ScentListCtrl', ['$scope', '$http', '$cookies', '$interval', 'Scents',
    function ($scope, $http, $cookies, $interval, Scents) {

    $scope.scents = null;
    $scope.newScents = null;
    $scope.updateScentsTimer = null;
    $scope.hasMoreScents = true;

    $scope.updateScents = function(firstScentId, lastScentId) {
        if ($scope.currentFence != null) {
            if (firstScentId != -1) {
                Scents.query({fence_id:$scope.currentFence.id,
                              first_scent_id:firstScentId}, function(scents){
                    $scope.newScents = scents;
                });
            } else if (lastScentId != -1) {
                Scents.query({fence_id:$scope.currentFence.id,
                              last_scent_id:lastScentId}, function(scents){
                    if (scents.length > 0)
                        $scope.scents = $scope.scents.concat(scents);
                    else
                        $scope.hasMoreScents = false;
                });
            }
            else {
                $scope.newScents = null;
                Scents.query({fence_id:$scope.currentFence.id}, function(scents){
                    $scope.scents = scents;
                });
            }
        } else {
            $scope.scents = null;
            $scope.newScents = null;
        }
    };

    $scope.$watch('currentFence', function(newFence, oldFence){
        $scope.hasMoreScents = true;
        $scope.updateScents(firstScentId=-1, lastScentId=-1);
        if (newFence == null) {
            if ($scope.updateScentsTimer != null) {
                $interval.cancel($scope.updateScentsTimer);
                $scope.updateScentsTimer = null;
            }
        }
        else if ($scope.updateScentsTimer == null) {
            $scope.updateScentsTimer = $interval(function() {
                $scope.updateScents(firstScentId=($scope.scents.length > 0 ? $scope.scents[0].id : -1),
                    lastScentId=-1);}, 5000);
        }
    });

    $scope.dropScent = function () {
        if ($scope.currentFence != null) {
            var data = {content:$scope.newScentText};
            // TODO: do this using Angular service
            $http({method:'POST', url: '/api/scents/', data: data,
                params: {fence_id:$scope.currentFence.id},
                headers: {'X-CSRFToken':$cookies.csrftoken}}).
              success(function(data, status, headers, config) {
                $scope.updateScents(firstScentId=($scope.scents.length > 0 ? $scope.scents[0].id : -1),
                    lastScentId=-1);
                $scope.newScentText = '';
              }).
              error(function(data, status, headers, config) {
                // TODO: I guess we don't show this to the user, but email?
                $scope.dropScentError = data.errors;
              });
        }
        else {
            alert("Sorry, but you need select a fence first.");
        }
    }

    $scope.getMoreScents = function () {
        $scope.updateScents(firstScentId=-1,
            lastScentId=($scope.scents.length > 0 ? $scope.scents[$scope.scents.length - 1].id : -1));
    }

    $scope.showNewScents = function() {
        $scope.scents = $scope.newScents.concat($scope.scents);
        $scope.newScents = null;
    }

}]);