$(document).on('keypress', 'input,select', function(e) {
    if (e.which == 13) {
        e.preventDefault();
        // Get all focusable elements on the page
        var $canfocus = $(':focusable');
        var index = $canfocus.index(this) + 1;
        if (index >= $canfocus.length) index = 0;
        $canfocus.eq(index).focus();
    }
});

var allMarkers = [];
$("#leg_boxes").on('keydown', 'input,select', function(e) {
    var keyCode = e.keyCode || e.which;
    console.log("you event !!!!")

    if (keyCode == 9) {
        console.log("you tabbed !!!!")
        console.log(this.value);
        if (!is_valid_airfield('K' + this.value.toUpperCase())) {
          this.value = ''
          return
        }
        //validate last input (or all inputs), if it isn't valid, return, don't create a new box.
        var textbox = document.createElement('input');
        var linebreak = document.createElement("br");
        textbox.type = "text"
        textbox.name = "waypoint"
        //textbox.attr("class","get_only_one")
        var att = document.createAttribute("class");       // Create a "class" attribute
        att.value = "get_only_one";                           // Set the value of the class attribute
        textbox.setAttributeNode(att);

        textbox.style = "text-transform:uppercase"
        textbox.focus
        document.getElementById('leg_boxes').appendChild(textbox)
        document.getElementById('leg_boxes').appendChild(linebreak)

        // ============================================================
        $.each($(".get_only_one"),function(i,e)
            {if(e.value > ""){
            airportID = "K" + e.value.toUpperCase()
            $.ajax({type: "GET",
                    url: '/instant_plot/',
                    data : {'airportID': airportID},
                    traditional: true,
                }).done(function(quickMarker) {
                    plot_on_map(quickMarker)
                })
            }
        })
    }
});

function plot_on_map(quickMarker){
    // var res = quickMarker.split("-");
    // qLatMarker = parseFloat(res[0])
    // qLonMarker = -parseFloat(res[1])
    var infoWindow = new google.maps.InfoWindow({
      content: '' + quickMarker.name
    });
    var newMarker = new google.maps.Marker({
      position: new google.maps.LatLng(quickMarker.latitude, quickMarker.longitude),
      icon: 'http://maps.google.com/mapfiles/ms/icons/green.png',
      draggable: true,
      map: map,
    });

    allMarkers.push(newMarker)

    map.panTo(newMarker.getPosition());

    if(allMarkers.length > 1){
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < allMarkers.length; i++) {
         bounds.extend(allMarkers[i].getPosition());
            }
        map.fitBounds(bounds);
    }

    newMarker.addListener('click', function() {
      infoWindow.open(map, newMarker);
    })
}

var airfields = [];
$.ajax({type: "GET",
        url: '/airfields/',
        traditional: true,
    }).done(function(response) {
        airfields = response
    })


function is_valid_airfield(identifier) {
  return airfields.indexOf(identifier) != -1
}
