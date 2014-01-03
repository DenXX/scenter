function initializeMaps() {
  var mapOptions = {
    zoom: 15,
    center: new google.maps.LatLng(33.7920235, -84.325642),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    mapTypeControl: false
  };

  var map = new google.maps.Map($('#map-canvas').get(0), mapOptions);

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
  drawingManager.setMap(map);
}