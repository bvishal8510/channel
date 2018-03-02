import json

code1 = 0

class ClientError(Exception):
    def init(self, code):
        print("Till here works fine")
        super(ClientError, self).init(code)
        self.code = code
        code1 = self.code


    def send_to(self, channel):
        channel.send({
            "text": json.dumps({
                "error": code1,
            }),
        })