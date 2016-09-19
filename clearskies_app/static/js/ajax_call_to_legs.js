wypts = []
$("#get_all").on('click', function() {
    $.each($(".get_only_one"),function(i,e)
        {if(e.value > "")
            {wypts.push(e.value)}
    })

mydata={'waypoint': wypts}
console.log(mydata);
$.ajax({type: "GET",
        url: '/fp/',
        data : mydata,
        traditional: true,
    }).done(function(weatherStations) {
            console.log(weatherStations);
            weatherStations.forEach(function(weatherStation) {
              plot_on_map(weatherStation.latitude + "" + weatherStation.longitude)
                console.log('identifier:', weatherStation.identifier)
                console.log('lat:', weatherStation.latitude)
                console.log('lon:', weatherStation.longitude)
                console.log('cloud_bases:', weatherStation.ceiling)
            })
        })
});
