"""

errors.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone

Licensed under the Apache License 2.0

"""

import discord
from data import config


class Errors:
    def __init__(self, *, client: discord.Client) -> None:
        self.client = client
        self.log_channel = client.get_channel(config.DISCORD_BOT_DATA["logChannelId"])

    def exception(self, *, error: Exception) -> None:
        """例外処理"""
        self.exception_log_message_send(error=error)

    def exception_log_message_send(self, *, error: Exception) -> None:
        """例外をDiscordチャンネルへ送信"""
        embed = self.embed_of_exception(err_code=0x0202, text="", error=error)
        self.log_channel.send(embed=embed)

    def embed_of_exception(
        self, *, err_code: int, text: str = "", error: Exception
    ) -> discord.Embed:
        """例外表示用のembedを生成

        Args:
            err_code (int): エラーコード。16進数として取り扱う。0x形式で記述
            text (str): 表示する説明文
            error (Exception)

        Returns:
            discord.Embed: 生成したembed
        """
        embed = discord.Embed(
            title="Error", description=f"{text}\n```{error}```", color=0xF04040
        ).set_footer(text=f"Error Code: {hex(err_code)}")
        return embed

    def embed_of_unhandled_exception(self, *, error: Exception) -> discord.Embed:
        """ハンドルされない例外表示用のembedを生成"""
        embed = self.embed_of_exception(
            err_code=0x0201, text="ハンドルされない例外が発生しました。", error=error
        )
        return embed
