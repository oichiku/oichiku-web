$(function() {
    $('#menu-checkbox').click(function() {
        if ($(this).prop('checked') == true) {
            $('.menu-button').addClass('is-active');
        } else {
            $('.menu-button').removeClass('is-active');
        }
    });
});
