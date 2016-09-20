wypts = []
document.getElementById("corridor_width").defaultValue = 0.2;
$("#get_all").on('click', function() {
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
            weatherStations.forEach(function(weatherStation) {
                var $item = $('<li></li>')
                var $ceiling = $('<ul></ul>')
                plot_on_map(weatherStation);
                console.log('identifier:', weatherStation.identifier);
                console.log('lat:', weatherStation.latitude);
                console.log('lon:', weatherStation.longitude);
                console.log('cloud_bases:', weatherStation.ceiling);
                $('#cber').append($item);
                $item.append(weatherStation.identifier)
                $item.append($ceiling)
                weatherStation.ceiling.forEach(function(text) {
                  $ceiling.append('<li>' + text + '</li>');
                });
            });
        });
});
