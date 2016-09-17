$('#addField').click(function(event) {
  event.preventDefault();
  $('.ui-widget').append('<li><input name="waypoint" class="tags"><button class="remove"><img src="../img/deleteglyph.svg"></button></li>');
  $('.tags').on("focus", function(){
    $(this).autocomplete({
     minLength: 2,
     source: availableTags
      });
    });
  $('.remove').click(function(event) {
    event.preventDefault();
    console.log('Hello');
    $(this).prev().remove();
    $(this).parent().remove()
    $(this).remove();
  });
})
