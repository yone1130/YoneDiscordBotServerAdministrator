"""

config.py | data | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

__title__ = "Yone Discord Bot Server Administrator"
__author__ = "よね/Yone"
__copyright__ = "Copyright 2022-2023 よね/Yone"
__license__ = "Apache License 2.0"

TOKEN = ""

MAIN_GUILD_ID = 0

DATABASE_FILE_PATH = "bot-savedata.db"

"""
以下サーバーごとのデータ。形式は下記の通り

dict = {
    サーバーID: データ (チャンネルID等)
}
"""
# Welcome Channels
welcomeChannels = {
}

# Notification channels when a member joins
joinedChannels = {
}

# Rule Channels
ruleChannels = {
}

# Member Role
memberRoles = {
}

# Notification channels when spam is detected
spamChannels = {
}

# Voice alert channel
voiceAlertChannel = {
}
