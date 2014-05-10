$(function() {
    $.get('/tagovi', {csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}, function(data) {
        var options = []
        for (var i = 0; i < data.length; i++) {
            options.push(data[i].fields);
        }
        $('#search').selectize({
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
});