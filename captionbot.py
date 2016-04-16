import sys
import telepot
from telepot.delegate import per_chat_id, create_open

class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(MessageCounter, self).__init__(seed_tuple, timeout)
        self._video = 0

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'video':
            self._video = msg['video']['file_id']
            self.sender.sendMessage("Great, now send the caption for this video!")
        elif content_type == 'text':
            if self._video != 0:
                self.sender.sendVideo(self._video, caption=msg['text'])
            else:
                if msg['text'].startswith('/'):
                    if msg['text'] == '/start':
                        self.sender.sendMessage("Hey, you can use this bot to put captions on videos! Just send a video first and then the caption you want to use.")
                    else:
                        self.sender.sendMessage("I'm sorry, I don't know what to do with this command!")
                else:
                    self.sender.sendMessage("First send a video and then send a caption to go with it!")

TOKEN = 'YOUR_TOKEN_HERE' 

bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(MessageCounter, timeout=10)),
])
bot.notifyOnMessage(run_forever=True)
