$(document).ready(function() {
    $("#reload").on("click", function(event) {
        event.preventDefault();
        $.get('/vise-recepata', {page: $("#page").val()}, function(data) {
            $("#toreload").remove();
            $("#content").append(data);
        });
    });
});