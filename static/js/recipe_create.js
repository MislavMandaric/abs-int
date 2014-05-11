$(document).ready(function() {
    $.get('/tagovi', function(data) {
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
});