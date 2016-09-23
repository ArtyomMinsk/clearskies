//wypts = []
document.getElementById("corridor_width").defaultValue = 0.2;
$("#get_all").on('click', function() {
    slide();
    google.maps.event.trigger(map, 'resize');
    var wypts = []
    $.each($(".get_only_one"),function(i,e)
        {if(e.value > "")
            {wypts.push("K" + e.value.toUpperCase())}
    })

mydata={'waypoint': wypts, 'corridor_width': $("#corridor_width").val()}
console.log(mydata);
$.ajax({type: "GET",
        url: '/fp/',
        data : mydata,
        traditional: true,
    }).done(function(weatherStations) {
            console.log(weatherStations);
            $('#cber').children().remove();
            console.log('Removed #cber children')
            weatherStations.forEach(function(weatherStation) {
                var $item = $('<li></li>')
                var $ceiling = $('<ul></ul>')
                colored_markers_on_map(weatherStation);
                $('#cber').append($item);
                $item.append(weatherStation.identifier + '-' + weatherStation.name)
                $item.append($ceiling)
                weatherStation.ceiling.forEach(function(text) {
                  $ceiling.append('<li>' + text + '</li>');
                });
            });
        });
});

function colored_markers_on_map(weather){
    reports = weather.ceiling.length
    count = 0
    while (count < reports) {
        wreport = weather.ceiling[count]
        layer = wreport.split(" ", 4)
        if (layer[0] == "Overcast"){ var lowestClouds = parseInt(layer[2])
            count = reports}
        if (layer[0] == "Broken"){ var lowestClouds = parseInt(layer[3])
            count = reports}
        if (layer[0] == "Clear"){ var lowestClouds = 'CLR'; count = reports}
        if (layer[0] == "Scattered"){
            if (layer[3] < 2000){ var lowestClouds = 2500 } else
            { var lowestClouds = 5000 } }
        if (layer[0] == "Few"){ var lowestClouds = 5000}

        var mrkColor = "http://maps.google.com/mapfiles/ms/icons/grey.png"
        if (lowestClouds < 500){mrkColor = "http://maps.google.com/mapfiles/ms/icons/red.png"}
        if (lowestClouds > 400 && lowestClouds < 1000){mrkColor = "http://maps.google.com/mapfiles/ms/icons/orange.png"}
        if (lowestClouds > 900 && lowestClouds < 1600){mrkColor = "http://maps.google.com/mapfiles/ms/icons/yellow.png"}
        if (lowestClouds > 1500 && lowestClouds < 2600){mrkColor = "http://www.googlemapsmarkers.com/v1/008000/"}
        if (lowestClouds > 2500 && lowestClouds < 5000){mrkColor = "http://maps.google.com/mapfiles/ms/icons/green.png"}
        if (lowestClouds > 4900 && lowestClouds < 10000){mrkColor = "http://www.googlemapsmarkers.com/v1/00e64d/"}
        if (lowestClouds == 'CLR') {mrkColor = "http://www.googlemapsmarkers.com/v1/66d9ff"}
        var infoWindow = new google.maps.InfoWindow({
          content: weather.identifier + ': ' + weather.name + '<br>Latitude: ' + weather.latitude + '<br>Longtitude: ' + weather.longitude
        });
        var newMarker = new google.maps.Marker({
          position: new google.maps.LatLng(weather.latitude, weather.longitude),
          icon: mrkColor,
          draggable: true,
          map: map,
          wID: weather.identifier
        });

        newMarker.addListener('click', function() {
          infoWindow.open(map, newMarker);
        });

        newMarker.addListener('mouseover', function() {
            console.log(newMarker.wID)
            highLightData(newMarker.wID, "yes")
        });

        newMarker.addListener('mouseout', function() {
            console.log('bye');
            highLightData(newMarker.wID, "no")

        });

        count++;
    }
    if(allMarkers.length > 1){
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < allMarkers.length; i++) {
         bounds.extend(allMarkers[i].getPosition());
            }
        map.fitBounds(bounds);
    }
}

function highLightData(wID, yesNo){
    var allData = document.getElementById("cber").getElementsByTagName("LI");
        for (i = 0; i < allData.length+1; i++) {
            if(allData[i].firstChild.data == wID){
                console.log("found it")
                if(yesNo == "yes"){ allData[i].style.backgroundColor = "gray"
                                    allData[i].style.fontWeight = "bolder"
                                    allData[i].style.color = "white"
                } else {
                    allData[i].style.backgroundColor = "ghostwhite"
                    allData[i].style.fontWeight = "normal"
                 }
                }
            }
        }
function slide(){
    $('.sidebar-first').hide(800);
    $('.sidebar-second').show(800);
    google.maps.event.trigger(map, 'resize');
}
