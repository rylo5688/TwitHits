var apiKey = "https://maps.googleapis.com/maps/api/js?key=" + GoogleKeys["key"] + "&callback=initMap&libraries=drawing,geometry";
function loadScript() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = apiKey;
    document.body.appendChild(script);
}

window.onload = loadScript;
var map;
var selected;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        // Boulder area
        center: new google.maps.LatLng(40.0068,-105.2628),
        mapTypeId: 'terrain'
    });

    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.RECTANGLE,
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['rectangle'],
            drawingModes: [google.maps.drawing.OverlayType.RECTANGLE]
        },
        rectangleOptions: {
            fillColor: '#ff0000',
            fillOpacity: 0.03,
            strokeWeight: 1,
            clickable: true,
            draggable: true,
            editable: true,
            deletable: true,
            zIndex: 1
        },
        markerOptions: {icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'}
    });

    // Allows for only one circle selection at a time
    google.maps.event.addListener(drawingManager, 'rectanglecomplete', function( rectangle ) {
        clearSelection();
        selected = rectangle;
    });

    // External Click clears out existing selections
    google.maps.event.addListener(map, 'click', function() {
        clearSelection();
    });

    drawingManager.setMap(map);
}

function clearSelection() {
    if ( selected ) {
        console.log("Updating selected area");
        selected.setMap(null);
        google.maps.event.clearInstanceListeners(selected);
    }
    selected = null;
}

// Called when "Generate Map" button is pressed
// Right now, just fits the Google Map view to selection
function genMap() {
    if( selected ) {
        console.log("Area is selected");
        var bounds = selected.getBounds();
        map.fitBounds( bounds );

        var northEast = bounds.getNorthEast();
        var southWest = bounds.getSouthWest();
        var heightCoords = northEast.lat() - southWest.lat();
        var widthCoords = northEast.lng() - southWest.lng();

        var northWest = new google.maps.LatLng( northEast.lat(), southWest.lng());
        var southEast = new google.maps.LatLng( southWest.lat(), northEast.lng());

        var heightKM = google.maps.geometry.spherical.computeDistanceBetween(northEast, southEast) / 1000;
        var widthKM = google.maps.geometry.spherical.computeDistanceBetween(northEast, northWest) / 1000;

        var tileHeightCoords = heightCoords / 5;
        var tileHeightKM = heightKM / 5;

        var tileWidthCords = widthCoords / 5;
        var tileWidthKM = widthKM / 5;

        var radiusKM = Math.min(tileHeightKM, tileWidthKM) / 2;

        var coords = [];
        //coords.push(radiusKM);

        var start = {lat: northWest.lat(), lng: northWest.lng()};
        for( i = 1; i < 5; i++ ) {
            for( j = 1; j < 5; j++ ) {
                var coord = { lat: start.lat + i*tileHeightKM, lng: start.lng + j*tileWidthKM };
                coords.push( coord )
            }
        }
        for( i = 0; i < coords.length; i++) {
            console.log("Lat: " + coords[i].lat + " Long: " + coords[i].lng);
        }
        //console.log("Radius: " + (Math.min(tileHeight, tileWidth) / 2));
        clearSelection();
    }
}

// Going back to default after query
function resetMap() {
    clearSelection();
    initMap();
}