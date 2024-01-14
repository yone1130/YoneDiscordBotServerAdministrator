"""

Yone Discord Bot Server Administrator

Copyright (c) 2022-2024 よね/Yone

Licensed under the Apache License 2.0.

"""

__title__ = "Yone Discord Bot Server Administrator"
__author__ = "よね/Yone"
__copyright__ = "© 2022-2024 よね/Yone"
__license__ = "Licensed under the Apache License 2.0"

APPLICATION_FILES = [
    "errors.py",
    "bot/commands.py",
    "bot/events.py",
    "database.py",
    "voice_channel_check.py",
]

DISCORD_BOT_DATA = {
    "token": "",
    "databaseFilePath": "bot-savedata.db",
    "logChannelId": 1119249005709365250,
    "ownerUserId": 892376684093898772,
    "mainGuildId": 1053378444781703339,
    "reportPostChannelId": 1062270394482053160,
}

"""
以下サーバーごとのデータ。形式は下記の通り

dict = {
    サーバーID: データ (チャンネルID等)
}
"""
# Welcome Channels
welcomeChannels = {
    1117201319946620989: 1117203236693225473,  # SoraNuemoNの雑談サーバー
}

# Notification channels when a member joins
joinedChannels = {
    1053378444781703339: 1053378446627188779,  # よね/Yoneのサーバー
    1020336203360370830: 1021050759086870550,  # Yone Discord Bot Service
    1083295375265378314: 1083315800615694446,  # YDITS
    1067751035340324946: 1068549790968852500,  # YDITS Project
    1053360115417354401: 1053360115417354404,  # Noachanの雑談サーバー
    1117201319946620989: 1117215352523345970,  # SoraNuemoNの雑談サーバー
}

# Rule Channels
ruleChannels = {
    1117201319946620989: 1117204442555633774,  # SoraNuemoNの雑談サーバー
}

# Member Role
memberRoles = {
    1117201319946620989: 1117201979580624937,  # SoraNuemoNの雑談サーバー
}

# Notification channels when spam is detected
spamChannels = {
    1053378444781703339: 1062270394482053160,  # よね/Yoneのサーバー
    1020336203360370830: 1062270394482053160,  # Yone Discord Bot Service
    1083295375265378314: 1062270394482053160,  # YDITS
    1067751035340324946: 1062270394482053160,  # YDITS Project
}

# Voice alert channel
voiceAlertChannel = {
    1053378444781703339: 1053378446102908953,  # よね/Yoneのサーバー
    1118704501084397577: 1118704733562097746,  # Yone Test Server
}
