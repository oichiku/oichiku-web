$(window).scroll(function() {
    if ($(window).scrollTop() > $(window).height()) {
        $('header').addClass('backgroundOn');
        $('.oideyo').hide();
    } else {
        $('header').removeClass('backgroundOn');
        $('.oideyo').show();
    }
})