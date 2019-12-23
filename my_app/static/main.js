function toggleMenu(buttId, menuId){

  if(buttId=='a-topic'){
    $('#' + menuId).removeClass('menuDisabled')
    $('#' + menuId).addClass('menuEnabled');
    // $('#' + menuId ).toggleClass('menuDisabled');
    // $('#' + menuId ).toggleClass('menuEnabled');
    // setTimeout(1000);
  }
}
function hideMenu(buttId, menuId){
  $('#' + menuId).removeClass('menuEnabled')
  $('#' + menuId).addClass('menuDisabled');
}


$(document).ready(function() {
  $('body').hide();
  $('body').fadeIn('slow/400/fast', function() {
  });

  $('#a-topic, #topic-dropdown').mouseover(function(){
    toggleMenu('a-topic','topic-dropdown');
  })
  $('#topic-dropdown').mouseleave(function(event) {
    hideMenu('a-topic','topic-dropdown');
  });

});
