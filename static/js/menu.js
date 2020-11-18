$(function() {
    $('#menu-checkbox').click(function() {
        if ($(this).prop('checked') == true) {
            $('.menu-button').addClass('is-active');
            $('body').css('overflow', 'hidden');
        } else {
            $('.menu-button').removeClass('is-active');
            $('body').css('overflow', '');
        }
    });
});