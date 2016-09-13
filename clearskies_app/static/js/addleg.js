// var $legfield = $('<input type="text" class="tags">');
var counter = 1;

$('#addleg').click(function() {
  if (counter < 5) {
    var $legfield = $('<input type="text" class="tags">');
    $legfield.attr('id','leg'+counter)
    $('#legs').append($legfield);
    console.log(counter);
  };
  counter++;
})
