$(document).ready(function(){
    $(".create_room").on('keypress', function(event) {
        key = event.keyCode;
        if (key == 13) {
            var name;
            name = $(this).val();
            console.log(name);
            $(this).val('');
            if (name != ''){
            $.get('/create_room/', {'name':name}, function (data) {
                var data1 =  JSON.parse(data);
                $('#room_user').attr({ "data-room-id" : data1[id] });
                console.log(data1);
                console.log(data1['name']);
                $('#room_user').append("<br><br>");
                $('#room_user').append(data1['name']);
                $('#room_user').append("<br>");
                console.log(data1['id']);
                // for (x in data1) {
                //     $('.room'+ data1['id']).append(data1['name']);
                //     $('.room'+ data1['id']).append("<br>");
                //     }
                })
            }
        }
    })
});

$(function () {
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);

    // Helpful debugging
    socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };

    socket.onmessage = function (message) {
        console.log("Got websocket message " + message.data);
        var data = JSON.parse(message.data);
        console.log(12);
        // Handle errors
        if (data.error) {
            alert(data.error);
            return;
        }
        // Handle joining
        if (data.join) {
            console.log("Joining room " + data.join);
            var roomdiv = $(
                "<div class='room' id='room-" + data.join + "' style='border: 2px solid green;'>"+
                "<center><h2 style='background-color:light-blue; font-size: xx-large; color:white;'><i>"
                 + data.title + "</i></h2></center>"+"<br>"+
                "<div class='messages" + data.join + "'></div>" +
                "<div class='messages' style='background-color:white;'></div>" +
                "<input><button class='btn btn-success' >Send</button>" +
                "</div>"
            );
            $("#chats").append(roomdiv);
            for (x in data.d) {
                $('.messages'+data.join).append("<p style='color:brown;display:inline;'>"+data.d[x][1]+"</p>");
                $('.messages'+data.join).append("&emsp;&emsp;&emsp;");
                $('.messages'+data.join).append("<p style='display:inline;'><i>"+data.d[x][0]+"</i></p>");
                $('.messages'+data.join).append("<br>");
    }

            console.log(13);
            roomdiv.find("button").on("click", function () {
                socket.send(JSON.stringify({
                    "command": "send",
                    "room": data.join,
                    "message": roomdiv.find("input").val()
                }));
                roomdiv.find("input").val("");
            });
            // Handle leaving
        } else if (data.leave) {
            console.log("Leaving room " + data.leave);
            $("#room-" + data.leave).remove();
        } else if (data.message || data.msg_type != 0) {
            var msgdiv = $("#room-" + data.room + " .messages");
            var ok_msg = "";
            switch (data.msg_type) {
                case 0:
                    // Message
                    ok_msg = "<div class='message'>" +
                        "<span class='username'>" + data.username + "</span>" +
                        "<span class='body'>" + data.message + "</span>" +"<br>"+
                        "</div>";
                    break;
                case 1:
                    // Warning/Advice messages
                    ok_msg = "<div class='contextual-message text-warning'>" + data.message + "</div>";
                    break;
                case 2:
                    // Alert/Danger messages
                    ok_msg = "<div class='contextual-message text-danger'>" + data.message + "</div>";
                    break;
                case 3:
                    // "Muted" messages
                    ok_msg = "<div class='contextual-message text-muted'>" + data.message + "</div>";
                    break;
                case 4:
                    // User joined room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username + " joined the room!" + "</div>";
                    break;
                case 5:
                    // User left room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username + " left the room!" + "</div>";
                    break;
                default:
                    console.log("Unsupported message type!");
                    return;
            }
            msgdiv.append(ok_msg);
            msgdiv.scrollTop(msgdiv.prop("scrollHeight"));
        } else {
            console.log("Cannot handle message!");
        }
    };

    // Says if we joined a room or not by if there's a div for it
    function inRoom(roomId) {
        return $("#room-" + roomId).length > 0;
        console.log(14);
    };

    // Room join/leave
    $("li.room-link").click(function () {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            // Leave room
            console.log(15);            
            $(this).removeClass("joined");
            socket.send(JSON.stringify({
                "command": "leave",  // determines which handler will be used (see chat/routing.py)
                "room": roomId
            }));
        } else {
            // Join room
            console.log(16);
            $(this).addClass("joined");
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
    });

    $("#room_user").click(function () {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            // Leave room
            console.log(15);            
            $(this).removeClass("joined");
            socket.send(JSON.stringify({
                "command": "leave",  // determines which handler will be used (see chat/routing.py)
                "room": roomId
            }));
        } else {
            // Join room
            console.log(16);
            $(this).addClass("joined");
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
    });
});