$(window).scroll(function() {
    var distanceTop = 50;
    if ($(window).scrollTop() > distanceTop) {
        $('div.pullup').fadeOut();
    } else {
        $('div.pullup').fadeIn("fast");
    }

    if ($(window).scrollTop() > $(window).height()) {
        $('header').addClass('backgroundOn');
        $('.oideyo').hide();
    } else {
        $('header').removeClass('backgroundOn');
        $('.oideyo').show();
    }
})