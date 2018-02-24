var map;
function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
 		zoom: 2,
		center: new google.maps.LatLng(40.0068,-105.2628),
		mapTypeId: 'terrain'
	});

	// Create a <script> tag and set the USGS URL as the source.
	var script = document.createElement('script');
    // This example uses a local copy of the GeoJSON stored at
    // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
    script.src = 'https://developers.google.com/maps/documentation/javascript/examples/json/earthquake_GeoJSONP.js';
    document.getElementsByTagName('head')[0].appendChild(script);
	}

// Loop through the results array and place a marker for each
// set of coordinates.
window.eqfeed_callback = function(results) {
    for (var i = 0; i < results.features.length; i++) {
    	var coords = results.features[i].geometry.coordinates;
    	var latLng = new google.maps.LatLng(coords[1],coords[0]);
    	var marker = new google.maps.Marker({
        	position: latLng,
        	map: map
      	});
    }
}

var apiKey = "https://maps.googleapis.com/maps/api/js?key=" + GoogleKeys["key"];

function loadScript() {
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.src = apiKey;
		document.body.appendChild(script);
}

window.onload = loadScript;