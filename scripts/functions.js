function postData(latitude, longitude) {
    $.ajax({
        type: "POST",
        url: "/GeoTrend.py",
        data: { param: input },
        success: callbackFunc
    });
}

function callbackFunc(result){
    console.log("called back");
}
