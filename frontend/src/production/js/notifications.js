function addNotification(day, month, ago, title, author, desc) {
    const li = $('<li>').append(
        $('<div>')
            .addClass('block')
            .append(
                $('<div>')
                    .addClass("block_content")
                    .append(
                        titleDiv(title),
                        dateBox(day, month),
                        authorDiv(ago, author),
                        descripctionDiv(desc)
                    )
            )
    )

    $("#notification-center")
        .append(li);
}

function dateBox(day, month) {
    return $('<article>')
        .addClass("media event")
        .css("display", "inline")
        .append(
            $('<a>')
                .addClass("pull-left date")
                .append(
                    $('<p>')
                        .addClass("month")
                        .text(month)
                    ,
                    $('<p>')
                        .addClass("day")
                        .text(day)
                )
        )
}

function titleDiv(title) {
    return $('<h2>')
        .addClass("title")
        .css("display", "inline")
        .append(
            $('<a>')
                .text(title)
                .attr("href", "#")
        )
}

function authorDiv(ago, author) {
    return $('<div>')
        .addClass("byline")
        .append(
            $('<span>')
                .text(`${ago} ago`)
            ,
            $('<a>')
                .text(` by ${author}`)
        );
}

function descripctionDiv(desc) {
    return $('<p>')
        .addClass("day")
        .text(desc);
}