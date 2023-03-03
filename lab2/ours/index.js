document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "127.0.0.1";   // the IP address of your Raspberry PI
var current_message = "STOP";

function client_update_one(){
    const net = require('net');

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${current_message}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        console.log("Recevied from server: ")
        console.log(data.toString());
        // split the data by comma
        data = data.toString().split(",");
        // first item is car direction
        document.getElementById("direction").innerHTML = data[0];
        // second item is car speed
        document.getElementById("speed").innerHTML = data[1];
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {
    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        forward();
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        backward();
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        left();
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        right();
    }
}

// reset the key to the start state 
function resetKey(e) {
    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";

    stop();
}

// update data for every 50ms
function update_data_from_textbox(){
    current_message = document.getElementById("message").value;
}

function forward() {
    current_message = "FORWARD";
}

function backward() {
    current_message = "BACKWARD";
}

function left() {
    current_message = "LEFT";
}

function right() {
    current_message = "RIGHT";
}

function stop() {
    current_message = "STOP";
}
