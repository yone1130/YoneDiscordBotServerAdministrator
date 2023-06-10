"""

voice_channel_check.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import datetime
import discord


class Voice_channel_check:
    def __init__(self):
        self.data = {}

    def add(self, user: discord.User):
        self.data.update({user.id: [user, datetime.datetime.now()]})
        print("add")

    def remove(self, user: discord.User):
        self.data.pop(user.id, None)
        print("remove")

    def check(self, user: discord.User):
        if user.id in self.data.keys():
            return self.data[user.id]
        else:
            return None

    def check_all(self):
        return self.data.items()
