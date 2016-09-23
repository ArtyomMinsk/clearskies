// go back to edit entries user entered
$("#return").on('click', function() {
    $('.sidebar-second').hide(800);
    $('.sidebar-first').show(800);
    google.maps.event.trigger(map, 'resize');
})
