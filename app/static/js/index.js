var socket = io();

// socket.on('connect', function () {
//     socket.emit('get_numbers');
// });

socket.on('new_number', function (number) {
    $('.numbers ul').append(
        '<li>' + number + '</li>'
    )
});