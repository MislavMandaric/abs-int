$(function() {
    $.post('', {csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}, function(data) {
        $('#search').selectize({
            selectOnTab: true,
            hideSelected: true,
            maxItems: 5,
            options: data
        });
    });
});

