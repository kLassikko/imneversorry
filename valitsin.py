import random
import re
import datetime
import json
import hashlib

class Valitsin:
    def __init__(self):
        self.commands = {}

    def getCommands(self):
        return self.commands

    def makeDecision(self, bot, update, alternatives):
        now = datetime.datetime.now()
        data = [
            update.message.from_user.id,
            now.day,
            now.month,
            now.year,
            alternatives
        ]
        seed = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        rigged = random.Random(seed)
        if rigged.randint(0, 49) == 0:
            answers = ['Molemmat :D', 'Ei kumpaakaan >:(']
            bot.sendMessage(chat_id=update.message.chat_id, text=rigged.sample(answers, 1)[0])
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=rigged.sample(alternatives, 1)[0])

    def onkoPakko(self, bot, update, groups):
        now = datetime.datetime.now()
        data = [
            update.message.from_user.id,
            now.day,
            now.month,
            now.year,
            groups.group(1)
        ]
        seed = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        rigged = random.Random(seed)
        if rigged.randint(0, 1) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text='ei ole pakko {}'.format(groups.group(1)))
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='on pakko {}'.format(groups.group(1)))

    def messageHandler(self, bot, update):
        msg = update.message
        if msg.text is not None:
            vai = set(msg.text.lower().split()[1::2]) == {'vai'}
            pakko = re.match(r"^onko pakko ([^?]+)(\??)$", msg.text.lower(), re.IGNORECASE)
            if vai:
                self.makeDecision(bot, update, msg.text.lower().split()[::2])
            elif pakko:
                self.onkoPakko(bot, update, pakko)
