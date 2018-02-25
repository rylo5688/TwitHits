var apiKey = "https://maps.googleapis.com/maps/api/js?key=" + GoogleKeys["key"] + "&callback=initMap&libraries=drawing";
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
        drawingMode: google.maps.drawing.OverlayType.CIRCLE,
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['circle'],
            drawingModes: [google.maps.drawing.OverlayType.CIRCLE]
        },
        circleOptions: {
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
    google.maps.event.addListener(drawingManager, 'circlecomplete', function( circle ) {
        clearSelection();
        selected = circle;
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
        map.fitBounds( selected.getBounds() );
        clearSelection();
    }
}

// Going back to default after query
function resetMap() {
    clearSelection();
    initMap();
}