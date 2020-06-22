console.log("Service Worker Loaded...");

// self.addEventListener("push", e => {
//     const data = e.data.json();
//     console.log("Push Recieved...");
//     self.registration.showNotification(data.title, {
//         body: "Notified by Traversy Media!",
//         icon: "http://image.ibb.co/frYOFd/tmlogo.png"
//     });
// });

self.addEventListener('install', event => {
    console.log('V1 installing…');
});


self.addEventListener('push', function(event) {

    console.log("xddddd");

    self.registration.showNotification("xdddddddd", {
        body: "Notified by Traversy Media!",
        icon: "http://image.ibb.co/frYOFd/tmlogo.png"
    });
    // if (event.data) {
    //     console.log('Push event!! ', event.data.text())
    // } else {
    //     console.log('Push event but no data')
    // }
});



    // // 3. Stwórz tytuł i treśc notyfikacji. Uzyj danych z serwera
    // const message = {
    //     data: "xdddd"
    // }
    // const title = 'Niesamowita sprawa!';
    //
    // // 4. Stwórz notyfikację
    // const promiseChain = event.registration.showNotification(title, message);
    // // 5. Wywołaj notyfikację
    // event.waitUntil(promiseChain);

    // cache a cat SVG
    // event.waitUntil(
    //     // caches.open('static-v1').then(cache => cache.add('/cat.svg'))
    // );

//
// self.addEventListener('activate', event => {
//     console.log('V1 now ready to handle fetches!');
// });
//
// self.addEventListener('fetch', event => {
//     // const url = new URL(event.request.url);
//
//     // serve the cat SVG from the cache if the request is
//     // same-origin and the path is '/dog.svg'
//     if (url.origin == location.origin && url.pathname == '/dog.svg') {
//         // event.respondWith(caches.match('/cat.svg'));
//     }
// });
