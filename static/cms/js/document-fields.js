$(function() {
    $('.prepyme-field-currency').hide();
    $('.prepyme-field-active').hide();

    $('#id_to_render').click(function() {
        $('.prepyme-field-currency').slideToggle("fast");
        $('.prepyme-field-active').slideToggle("fast");
    });
});
