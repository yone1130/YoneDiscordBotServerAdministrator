"""

voice_channel_check.py | Yone Discord Bot Server Administrator

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import datetime
import discord


class Voice_channel_check:
    """ボイスチャンネルの入退出データ操作クラス"""

    def __init__(self) -> None:
        self.data = {}

    def add(self, user: discord.User) -> None:
        """データを追加"""
        self.data.update({user.id: [user, datetime.datetime.now()]})
        print("add")

    def remove(self, user: discord.User) -> None:
        """データを削除"""
        self.data.pop(user.id, None)
        print("remove")

    def check(self, user: discord.User) -> dict | None:
        """指定ユーザーのデータを取得"""
        if user.id in self.data.keys():
            return self.data[user.id]
        else:
            return None

    def check_all(self) -> dict.items:
        """全ユーザーのデータを取得"""
        return self.data.items()
