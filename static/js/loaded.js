$(window).on('load', function(){
    setTimeout(function(){
        $('.mask').fadeOut(500);
        $('body').css('overflow', 'scroll');
    }, 500);
});