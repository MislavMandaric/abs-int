$(document).ready(function() {
    $('#like').on( "click", function(event) {
        event.preventDefault();
        var id = $('#rp_id').val();
        $.get('/like?id=' + String(id), function(data) {
            $('#like').attr('disabled','disabled');
        });
    });
});