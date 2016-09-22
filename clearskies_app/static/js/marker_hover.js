var marker = new google.maps.Marker({
  map: map,
});


marker.addListener('mouseover', function() {
    marker.getPosition(who)
    console.log('who')
});

marker.addListener('mouseout', function() {
    infowindow.close();
});
