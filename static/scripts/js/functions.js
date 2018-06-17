var response = "";
function postData(lat, lng) {
  $.ajax({
     type: "GET",
     url: $SCRIPT_ROOT + "/nearbyTrends/",
     contentType: "application/json; charset=utf-8",
     async: false,
     data: {latitude : lat, longitude: lng},
     success: function(data) {
       console.log(data);
       response = "SUCCESS";
     }
 });

 return response;
    // console.log("test");
}
