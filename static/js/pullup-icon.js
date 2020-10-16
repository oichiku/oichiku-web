$(function() {
  $(window).scroll(function() {
    var distanceTop = 50;

    if ($(window).scrollTop() > distanceTop) {
      $('div.pullup').fadeOut();
    } else {
      $('div.pullup').fadeIn("fast");
    }
  });
});