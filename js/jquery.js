var var1;
jQuery(function(){
    $('body').fadeIn(1000);
    setTimeout(function(){
        $('body').fadeOut(1000, function(){
            location.reload(true);
        });
    }, 5000); // 5 seconds
});