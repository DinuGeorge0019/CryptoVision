

$(document).ready(function(){
    $(".coin_box").click(function(){
        // Remove the 'selected' class from all .coin_box elements
        $(".coin_box").removeClass('selected');

        // Add the 'selected' class to the clicked .coin_box element
        $(this).addClass('selected');
    });
});