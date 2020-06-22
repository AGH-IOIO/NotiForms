function refreshNotifications() {

    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    const {backend} = window.glob;

    if (backend && token) {
        $.ajax({
            type: "GET",
            url: `${backend}/messages/${username}/`,
            headers: {
                "Authorization": token
            },
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.messages) {
                    if (window.glob.forms) {
                        $("#notification-center li").remove();

                        console.log('xddddd11');
                        // console.log(data.messages);
                        processMessages(data.messages);
                        // data.messages.reverse().map(message => addMessage(message));
                    } else {
                        const messages = data.messages;
                        $.ajax({
                            type: "GET",
                            url: `${backend}/forms/pending/${username}/`,
                            headers: {
                                "Authorization": token
                            },
                            contentType: "application/json",
                            dataType: "json",
                            success: function (data) {
                                if (data.forms) {
                                    window.glob.forms = data.forms;
                                    $("#notification-center li").remove();
                                    // console.log('xddddd');
                                    // console.log(data.messages);
                                    processMessages(messages);
                                }
                            },
                            failure: function (errMsg) {
                                console.log(errMsg);
                            },
                        });
                    }
                }
            },
            failure: function (errMsg) {
                console.log(errMsg);
            },
        });
    }
}


function processMessages(messages) {

    let counter = 0;
    for (let i = messages.length - 1; i >= 0; i = i - 1) {
        addMessage(messages[i]);

        if (!messages[i].viewed) {
            counter++;
        }
    }
    $('span.badge:nth-child(2)').text(counter);
    // messages.reverse().map(message => addMessage(message));
}

function addMessage(message) {

    const forms = window.glob.forms;

    if (forms) {
        const matchedForm = forms.find(t => t._id === message.ref_id);
        addNotification('', '', '', matchedForm.title, matchedForm.template.owner, message.text, message.viewed, message._id);
    }
}

function addNotification(day, month, ago, title, author, desc, clicked, id) {

    const li = $('<li>')
        .append(
            $('<div>')
                .attr('id', id)
                .addClass('block')
                .append(
                    $('<div>')
                        .addClass("block_content")
                        .append(
                            titleDiv(title, id),
                            dateBox(day, month),
                            authorDiv(ago, author),
                            descripctionDiv(desc)
                        )
                )
        )

    if (clicked) {
        li.css('background', '#D9D9D6')
    }

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

function titleDiv(title, id) {
    return $('<h2>')
        .addClass("title")
        .css("display", "inline")
        .append(
            $('<a>')
                .text(title)
                .click(function () {
                    markAsViewed.call(this, id);
                })
        )
}

function markAsViewed(id) {

    const {backend} = window.glob;
    const token = localStorage.getItem('token');
    const owner = localStorage.getItem('username');


    if (backend && token && owner) {
        $.ajax({
            type: "POST",
            url: `${backend}/messages/mark_as_viewed/`,
            headers: {
                "Authorization": token
            },
            data: JSON.stringify({
                owner,
                ids: [id]
            }),
            contentType: "application/json",
            dataType: "json",
            success: function () {
                const li = $(`#${id}`);
                if (li.css("background") !== "") {
                    li.css("background", "");

                    const badge = $('span.badge:nth-child(2)');
                    const count = parseInt(badge.text()) - 1;
                    badge.text(count);

                }
            },
            failure: function (errMsg) {
                console.log(errMsg);
            },
        });
    }

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


function registerSWCall() {

    removeServiceWorkers();

    if (!window.Notification) {
        console.log('Browser does not support notifications.');
    } else if (Notification.permission === 'granted') {
        registerSW();
    } else {
        Notification.requestPermission().then(function (p) {
            if (p === 'granted') {
                registerSW();
            }
        });
    }
}

function registerSW() {
    const token = localStorage.getItem('token');
    const {backend} = window.glob;

    if (token && backend) {
        $.ajax({
            type: "GET",
            url: `${backend}/push/get_public_key/`,
            headers: {
                "Authorization": token
            },
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.public_key) {
                    registerServiceWorker(data.public_key);
                }
            },
            failure: function (errMsg) {
                console.log(errMsg);
            },
        });
    }
}

function registerServiceWorker(publicVapidKey) {

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

                    const token = localStorage.getItem('token');
                    const username = localStorage.getItem('username');
                    const {backend} = window.glob;

                    if (token && backend && username) {
                        $.ajax({
                            type: "POST",
                            url: `${backend}/push/subscribe/`,
                            headers: {
                                "Authorization": token
                            },
                            data: JSON.stringify({
                                username,
                                user_agent: navigator.userAgent,
                                subscription_info: pushSubscription
                            }),
                            contentType: "application/json",
                            dataType: "json",
                            success: function () {
                            },
                            failure: function (errMsg) {
                                console.log(errMsg);
                            },
                        });
                    }

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