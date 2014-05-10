$(function() {
    $.get('/tagovi', {csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}, function(data) {
        var options = []
        for (var i = 0; i < data.length; i++) {
            options.push(data[i].fields);
        }
        $('#id_tags').selectize({
            persist: false,
            maxItems: 5,
            selectOnTab: true,
            valueField: 'name',
            labelField: 'name',
            searchField: 'name',
            options: options,
            create: function (input) {
                return {
                    name: input
                };
            }
        });
    });

    $("#reload").on("click", function(event) {
        event.preventDefault();
        $.get('/vise-recepata', {page: $("#page").val(), csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}, function(data) {
            $("#toreload").remove();
            $("#content").append(data);
        });
    });
});