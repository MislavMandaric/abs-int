$(function() {
    $.post('/', {csrfmiddlewaretoken: $("hidden[name='csrfmiddlewaretoken']").next().text()}, function(data) {
        $('#search').selectize({
            selectOnTab: true,
            hideSelected: true,
            maxItems: 5,
            options: data,
        });
    });
});