self.addEventListener('install', event => {
    console.log('V1 installing…');
});

self.addEventListener('push', function(data) {

    self.registration.showNotification("xdddddddd", {
        body: "Notified by Traversy Media!",
    });
});
