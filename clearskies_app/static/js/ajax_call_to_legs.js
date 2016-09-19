wypts = []
$("#get_all").on('click', function() {
    $.each($(".get_only_one"),function(i,e)
        {if(e.value > "")
            {wypts.push(e.value)}
    })

mydata={'waypoint': wypts}
$.ajax({type: "POST",
        url: '/get_all/',
        data : mydata,
        traditional: true,
    }).done(function(weatherStations) {

            weatherStations.forEach(function(weatherStation) {
                console.log('identifier:', weatherStation.identifier)
                console.log('lat:', weatherStation.lat)
                console.log('lon:', weatherStation.lon)
                console.log('cloud_bases:', weatherStation.cloud_bases)
            })
        })
});
