var ws;
var user;
var host = null;
var pregame;
var user_id;

window.onload = function() {
    $.when( $.get('/user'), $.get('/pregame')).then(
        function(d1,d2) {
            user = d1[0].name;
            user_id = d1[0].id;
            pregame = d2[0].pregame;
        if (window.location.pathname != '/host') {
            $('.hand_area').load('/hand', function(data) {
                console.log('starting unslider');
                var hand_banner = $('.hand_banner');
                var slidey = hand_banner.unslider();
                data = slidey.data('unslider');
                data.dots();
            });
        } else {
            host = true;
            $('#hand_header').hide();
            $.get("/address", function (data) {
                    console.log(data);
                    if (pregame) {
                        console.log('callback called');
                        var join_header = $('#join_header');
                        join_header.text('Go to '
                        + data +
                        ' now!');
                        join_header.show();
                        user_id = '0000';
                        user = 'HOST';
                    }
            });
        }
        get_czar();
    });

};

function get_czar(){
    $.get("/czar", function (data) {
        var czar_header = $('#current_czar_header');
        var json_resp = data;
        if (json_resp['czar_chosen'] == true){
            czar_header.show();
            czar_header.text('Czar: ' + json_resp['czar']);
        }
        else{
            czar_header.hide();
        }
    });
}

$(document).ready(function(){
    namespace = '/ws'; // change to an empty string to use the global namespace
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        console.log('sending client message');
        socket.emit(
            'user_connected',
            data = { type: 'client_connect',
                     user_id: user_id,
                     user: user
                     }
        );
        return false;
    });

    socket.on('game_ready', function(msg) {
        // Show the 'Start Game' button when enough players
    });

    socket.on('no_host', function(event) {
        // Show 'Please wait for the game to be hosted' message
        document.cookie = 'username=; path=/; domain='+document.domain+'; expires=' + new Date(0).toUTCString();
    });

    socket.on('czar_chosen', function(event){
       // When server says czar is chosen, show this on the clients.
        get_czar();
    });

});
