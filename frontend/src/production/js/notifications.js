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

function pushNotification(msg){

    addNotification(12,"april", "witam", "michal", "tralalal wypelnij anikete prosze ja ciebie bo bedzie zle");

    let push = function (msg){
        new Notification('NotiForms', {
            body: msg,
            icon: "https://img.icons8.com/ultraviolet/80/000000/survey.png"
        });
    }

    if(!window.Notification){
        console.log('Browser does not support notifications.');

    } else if (Notification.permission === 'granted') {
        push(msg);
    } else{
        Notification.requestPermission().then(function(p) {
            if(p === 'granted') {
                push(msg);
            }
        });
    }


}