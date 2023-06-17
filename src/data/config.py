"""

config.py | data | Yone Discord Bot Server Administrator

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

__title__ = "Yone Discord Bot Server Administrator"
__author__ = "よね/Yone"
__copyright__ = "Copyright (c) 2022-2023 よね/Yone"
__license__ = "Apache License 2.0"

APPLICATION_FILES = [
    "./src/errors.py",
    "./src/bot/commands.py",
    "./src/bot/events.py",
    "./src/database.py",
    "./src/voice_channel_check.py",
]

DISCORD_BOT_DATA = {
    "token": "",
    "databaseFilePath": "bot-savedata.db",
    "logChannelId": 1119249005709365250,
    "ownerUserId": 892376684093898772,
    "mainGuildId": 1053378444781703339,
    "reportPostChannelId": 1062270394482053160
}

"""
以下サーバーごとのデータ。形式は下記の通り

dict = {
    サーバーID: データ (チャンネルID等)
}
"""
# Welcome Channels
welcomeChannels = {
    1053378444781703339: 1053378445616357429,  # よね/Yoneのサーバー
    1020336203360370830: 1021034964533395456,  # Yone Discord Bot Service
    1083295375265378314: 1083295587312611352,  # YDITS
}

# Notification channels when a member joins
joinedChannels = {
    1053378444781703339: 1053378446627188779,  # よね/Yoneのサーバー
    1020336203360370830: 1021050759086870550,  # Yone Discord Bot Service
    1083295375265378314: 1083315800615694446,  # YDITS
    1067751035340324946: 1068549790968852500,  # YDITS Project
    1053360115417354401: 1053360115417354404   # Noachanの雑談サーバー
}

# Rule Channels
ruleChannels = {
    1053378444781703339: 1053378446459412506,  # よね/Yoneのサーバー
    1020336203360370830: 1055440707353063434,  # Yone Discord Bot Service
    1083295375265378314: 1083296085214244904,  # YDITS
    1067751035340324946: 1067755178616442930,  # YDITS Project
}

# Member Role
memberRoles = {
    1053378444781703339: 1053378444781703343,  # よね/Yoneのサーバー
    1020336203360370830: 1020475074995830805,  # Yone Discord Bot Service
    1083295375265378314: 1083296756734889984,  # YDITS
    1067751035340324946: 1067758105938624532,  # YDITS Project
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
    1053378444781703339: 1053378446459412502,  # よね/Yoneのサーバー
    1053360115417354401: 1055203936040136788,  # Noachanの雑談サーバー
}
