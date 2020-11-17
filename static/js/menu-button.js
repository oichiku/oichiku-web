$(function() {
    $('#menu-checkbox').click(function() {
        $('.menu-button').toggleClass('is-active');
        if ($(this).prop('checked') == true) {
            $('body').css('overflow', 'hidden')
        } else {
            $('body').css('overflow', '')
        }
    });
});