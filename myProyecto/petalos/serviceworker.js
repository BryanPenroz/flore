var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/static/core/css/estilos.css',
    '/static/core/img/carritologo.png',
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request)
        .then(function(result){
            return caches.open(CACHE_NAME)
            .then(function(){
                caches.put(event.request.url,result.clone());
                return result;
            })
        })
        .catch(function(e){
            return caches.match(event.request)
        })
    );
});

//codigo para notificaciones push


importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');

var firebaseConfig = {
                apiKey: "AIzaSyAWuELTCOiWJbzeX14VEkYH8PRlXp1GQB0",
                authDomain: "floreria-c1504.firebaseapp.com",
                databaseURL: "https://floreria-c1504.firebaseio.com",
                projectId: "floreria-c1504",
                storageBucket: "floreria-c1504.appspot.com",
                messagingSenderId: "454939692114",
                appId: "1:454939692114:web:e1e8dad7cb612c4ee6638b"
            };
            // Initialize Firebase
            firebase.initializeApp(firebaseConfig);

            let messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload){

	let title = 'titulo de la notificacion';
	
	let options = {
		 body:'Este es el mensaje',
                 icon: '/static/img/logofb.png'

	}

	self.registration.showNotification(title, options);

});

