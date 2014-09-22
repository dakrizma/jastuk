$(document).ready(function() {

    if ( $('.error_message').length ) {

        $('.error_message').each(function( index ) {

            var greska = $(this).children('.wrap');

            if ( greska.text().length ) {

                $(this).fadeIn(200);

                $(this).on('click', function() {

                    $(this).fadeOut(200);

                });
            }
        });        
    }
});

