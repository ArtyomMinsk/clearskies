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

$("#leg_boxes").on('keydown', 'input,select', function(e) {
    var keyCode = e.keyCode || e.which;
    console.log("you event !!!!")

    if (keyCode == 9) {
        console.log("you tabbed !!!!")
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
            console.log(e.value)
            airportID = "K" + e.value
            $.ajax({type: "GET",
                    url: '/instant_plot/',
                    data : {'airportID': airportID},
                    traditional: true,
                }).done(function(quickMarker) {
                    console.log("YOU MADE IT TO A RETURN FROM POST")
                    console.log(quickMarker, "SSSSSSSSSSS")
                    plot_on_map(quickMarker)
                })
            }
        })
    }
});

function plot_on_map(quickMarker){
    var res = quickMarker.split("-");
    console.log(quickMarker)
    qLatMarker = parseFloat(res[0])
    qLonMarker = -parseFloat(res[1])
    var newMarker = new google.maps.Marker({
      position: new google.maps.LatLng(qLatMarker, qLonMarker),
      icon: 'http://maps.google.com/mapfiles/ms/icons/green.png',
      draggable: true,
      map: map
        })
}
