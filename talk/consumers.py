import json
from channels import Group, Channel
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import Room
from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError

@channel_session_user_from_http
def ws_connect(message):
    print(4)
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []


@channel_session_user
def ws_disconnect(message):
    print(5)
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass

def ws_receive(message):
    print(6)
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@catch_client_error
@channel_session_user
def chat_join(message):
    print(7)
    room = get_room_or_error(message["room"], message.user)
    print(132)
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_ENTER)
    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    print(dict(message))
    print(dict(message.channel_session))
    print(list(set(message.channel_session['rooms']).union([room.id])))
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })
    print(133)

@channel_session_user
@catch_client_error
def chat_leave(message):
    print(9)
    room = get_room_or_error(message["room"], message.user)
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })


@catch_client_error
@channel_session_user
def chat_send(message):
    print(10)
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)
    room.send_message(message["message"], message.user)

# @channel_session_user_from_http
# def ws_connect(message):
#     Group('users').add(message.reply_channel)
#     Group('users').send({
#         'text': json.dumps({
#             'username': message.user.username,
#             'is_logged_in': True
#         })
#     })


# @channel_session_user
# def ws_disconnect(message):
#     Group('users').send({
#         'text': json.dumps({
#             'username': message.user.username,
#             'is_logged_in': False
#         })
#     })
#     Group('users').discard(message.reply_channel)

# def ws_echo(message):
#     message.reply_channel.send({
#         'text': message.content['text'],
#     })