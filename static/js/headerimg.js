$(function() {
  $(window).scroll(function() {
    var distanceTop = 500;

    if ($(window).scrollTop() > distanceTop) {
      $('.headerimg').fadeIn();
    } else {
      $('.headerimg').fadeOut();
    }
  });
});
