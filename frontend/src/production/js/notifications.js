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

function removeServiceWorkers() {
    navigator.serviceWorker.getRegistrations().then(function (registrations) {
        for (let registration of registrations) {
            registration.unregister()
        }
    })
}

function registerServiceWorker() {

    const publicVapidKey = "BD7cSED3VxyrDftluX7KC9kU8YxTz1NYCVQRBPzxP9XGPG0SYFhJslgalUc4tbpKJ7mvfsccF9cOPo2iJ_FxDKg";

    navigator.serviceWorker.register('/serviceWorker.js');

    navigator.serviceWorker.ready.then(
        function (serviceWorkerRegistration) {
            var options = {
                userVisibleOnly: true,
                applicationServerKey: publicVapidKey
            };
            serviceWorkerRegistration.pushManager.subscribe(options).then(
                function (pushSubscription) {

                    console.log('Received PushSubscription: ', JSON.stringify(pushSubscription));
                    // The push subscription details needed by the application
                    // server are now available, and can be sent to it using,
                    // for example, an XMLHttpRequest.
                }, function (error) {

                    console.log(error);
                }
            );
        });
}

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/')
    ;
    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}

function pushNotification(msg) {

    removeServiceWorkers();

    // if (!window.Notification) {
    //     console.log('Browser does not support notifications.');
    // } else if (Notification.permission === 'granted') {
    //     registerServiceWorker();
    // } else {
    //     Notification.requestPermission().then(function (p) {
    //         if (p === 'granted') {
    //             registerServiceWorker();
    //         }
    //     });
    // }
}