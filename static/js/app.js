
var x = document.getElementById("demo");
function getLocation() {

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
      x.innerHTML = "Geolocation is not supported by this browser.";
    }
}
  
function showPosition(position) {
      // Saving lat and long in variables
      lat= position.coords.latitude
      long= position.coords.longitude
  
       x.innerHTML = "Latitude: " + position.coords.latitude + 
       "<br>Longitude: " + position.coords.longitude;
      url="https://apis.mapmyindia.com/advancedmaps/v1/fzzfsz7dejrhf5p41iuxd3rv95uoz1ve/rev_geocode?lat="+lat+"&"+"lng="+long
        

    //Sending the GET request to obtain JSON file and parse it to get the output
        $.ajax({
            type: "GET",
            dataType: 'json',
            url: url,
            async: true,
            // SameSite=None,
            data: {
                url: JSON.stringify(url),
            },
            //Processing JSON file once the request is successful
            success: function (result) {
                var jsondata = JSON.parse(result);
                if (jsondata.responseCode == 200) {

                    console.log(jsondata)

                        // sending values to the HTML doc 
                        var lat = jsondata.results[0].lat;
                        $("#Latitude").append(lat);
                        var lng = jsondata.results[0].lng;
                        $("#Longitude").append(lng);
                        var village = jsondata.results[0].village;
                        $("#Village").append(village);
                        var district = jsondata.results[0].district;
                        $("#District").append(district);
                        var state = jsondata.results[0].state;
                        $("#State").append(state);
                        
                }
                /*handle the error codes and put the responses in divs. more error codes can be viewed in the documentation*/
                else{
                   document.getElementById('result').innerHTML="No Result found" ;
                }
            }
        });
}
