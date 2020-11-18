$(window).scroll(function() {
    if ($(window).scrollTop() > $(window).height()) {
        $('header').addClass('backgroundOn')
    } else {
        $('header').removeClass('backgroundOn')
    }
})