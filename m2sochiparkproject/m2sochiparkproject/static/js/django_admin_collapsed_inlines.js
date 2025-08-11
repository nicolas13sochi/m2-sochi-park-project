jQuery(function($) {
    $('div.inline-group').each(function() {
        h2 = $(this).find('h2:first');
        var accordion = $(h2.nextAll('div'))
        var items = accordion.children();
        if (items.length > 2){
            items.addClass('unfold-accordion-item ');
            $.each(items, function() {
                if (!$(this).hasClass('empty-form')){
                    var h3 = $(this).find('h3:first');
                    var div_body = $(this).find('div:first');
                    h3.addClass('unfold-accordion-header');
                    div_body.addClass('unfold-accordion-body');
                    $(h3).click(function(e) {
                        if ($(this).parent().hasClass('unfold-accordion-item-show'))
                            $(this).parent().removeClass('unfold-accordion-item-show');
                        else
                            $(this).parent().addClass('unfold-accordion-item-show');
                    });
                }
            });
        }
    });
    
});
