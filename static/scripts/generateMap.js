var myLink = document.getElementById('mylink');
function genMap() {
	if( selected ) {
		console.log("Area is selected");
		console.log(selected.getBounds().getNorthEast());
	}
}