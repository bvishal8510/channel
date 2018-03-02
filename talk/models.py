from django.conf import settings
from django.db import models
from channels import Group
from django.utils.six import python_2_unicode_compatible
from .settings import MSG_TYPE_MESSAGE
import json

class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logged_in_user')

@python_2_unicode_compatible
class Room(models.Model):
    title = models.CharField(max_length=255)
    staff_only = models.BooleanField(default=False)

    def str(self):
        return self.title

    @property
    def websocket_group(self):
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):

        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )