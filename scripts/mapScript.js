var apiKey = "https://maps.googleapis.com/maps/api/js?key=" + GoogleKeys["key"];
function loadScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = apiKey;
    document.body.appendChild(script);
}

window.onload = loadScript;

var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: new google.maps.LatLng(40.0068,-105.2628),
        mapTypeId: 'terrain'
    });
    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.MARKER,
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['rectangle'],
            drawingModes: [google.maps.drawing.OverlayType.RECTANGLE]
        },
        rectangleOptions: {
            fillColor: '#ffffff',
            fillOpacity: 0.35,
            strokeWeight: 3,
            clickable: true,
            draggable: true,
            editable: true,
            zIndex: 1
        },
        markerOptions: {icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'}
    });
    drawingManager.setMap(map);
}