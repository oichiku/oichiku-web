$(window).on('load', function(){
    setTimeout(function(){
        $('.mask').fadeOut();
        $('body').css('overflow', 'scroll');
    }, 1000);
});