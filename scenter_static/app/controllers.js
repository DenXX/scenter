
var scenterControllers = angular.module('scenterControllers', []);

scenterControllers.controller('FenceCtrl', ['$scope', 'Fences', function ($scope, Fences) {
    var mapOptions = {
        zoom: 15,
        center: new google.maps.LatLng(33.7920235, -84.325642),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false
    };

    $scope.map = new google.maps.Map($('#map-canvas').get(0), mapOptions);
    $scope.polygons = {};
    $scope.current_polygon = null;
    $scope.infoWindow = null;

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

    $scope.getPolygonOptions = function (active) {
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

    $scope.selectFence = function (fence) {
        if ($scope.currentPolygon) {
            $scope.currentPolygon.setOptions($scope.getPolygonOptions(false));
        }

        $scope.currentPolygon = fence;
        $scope.currentPolygon.setOptions($scope.getPolygonOptions(true));
    };

    // TODO: If we move map and fence goes out of scope, we should remove window.
    $scope.showInfoWindow = function (fence, coords) {
        var contentString = '<div>' + fence.name + '</div>';
        if ($scope.infoWindow)
            $scope.infoWindow.close();
        $scope.infoWindow = new google.maps.InfoWindow({
            position: coords,
            content: contentString
        });
        $scope.infoWindow.open($scope.map);
    };

    // TODO: Create service for all this functions
    $scope.displayFence = function (fence) {
        if (fence.id in $scope.polygons)
            return;
        // Define the LatLng coordinates for the polygon's path.
        var vertices = new Array();
        var fence_location = JSON.parse(fence.location);
        for (var i = 0; i < fence_location.coordinates[0].length; ++i) {
            vertices.push(new google.maps.LatLng(fence_location.coordinates[0][i][0],
                fence_location.coordinates[0][i][1]));
        }
        fence_polygon = new google.maps.Polygon({paths: vertices});
        fence_polygon.setOptions($scope.getPolygonOptions(false));
        fence_polygon.id = fence.id;
        fence_polygon.name = fence.name;

        google.maps.event.addListener(fence_polygon, 'click', function(event){
            $scope.selectFence(this);
            $scope.showInfoWindow(this, event.latLng);
        });

        fence_polygon.setMap($scope.map);
        $scope.polygons[fence_polygon.id] = fence_polygon;
    };

    $scope.updateFences = function() {
        var boundingBox = $scope.map.getBounds();
        var map_bbox = boundingBox.getNorthEast().lat()+','+boundingBox.getNorthEast().lng()+
            ','+boundingBox.getSouthWest().lat()+','+boundingBox.getSouthWest().lng();
        Fences.query({bbox: map_bbox}, function(fences){
            fences.forEach($scope.displayFence);
        });
    };

    google.maps.event.addListenerOnce($scope.map, 'tilesloaded', function () {
        $scope.updateFences();
    });
    google.maps.event.addListener($scope.map, 'dragend', function () {
        $scope.updateFences();
    });
    google.maps.event.addListener($scope.map, 'zoom_changed', function () {
        $scope.updateFences();
    });
}]);
 
scenterControllers.controller('ScentListCtrl', ['$scope', '$http', function ($scope) {
  $scope.scents = [
    {'content': 'This is sample scent text. This is sample scent text. This is sample scent text. This is sample scent text. ',
     'fence': 'Emory University',
     'author': "DenXX"},
    {'content': 'I don\'t understand what you are saying. I don\'t understand what you are saying. I don\'t understand what you are saying. ',
     'fence': 'China',
     'author': "YuWang"},
    {'content': 'This is sample scent text. This is sample scent text. This is sample scent text. This is sample scent text. ',
     'fence': 'Emerson Hall',
     'author': "DavidFink"}
  ];
}]);