

$(document).ready(function() {
    $('.tab').click(function() {
        // Remove the 'active' class from all buttons
        $('.tab').removeClass('active');

        // Add the 'active' class to the clicked button
        $(this).addClass('active');

        var category = $(this).attr('data-category');
        $('.card').each(function() {
            if ($(this).data('category') === category) {
                $(this).css('display', 'block');
            } else {
                $(this).css('display', 'none');
            }
        });
    });
});


