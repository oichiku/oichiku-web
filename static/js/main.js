$(window).on('load', function() {
    setTimeout(function() {
        $('.mask').fadeOut(500);
        $('body').css('overflow', 'scroll');
    }, 500);
});

$(function() {
    $('#menu-checkbox').change(function() {
        if ($('#menu-checkbox').prop('checked')) {
            $('#rmFocus').removeClass('menuClosed');
            $('#rmFocus').addClass('menuOpen');
            $('body').css('overflow', 'hidden');
        } else {
            $('#rmFocus').removeClass('menuOpen');
            $('#rmFocus').addClass('menuClosed');
            $('body').css('overflow', 'scroll');
        }
    });
});
