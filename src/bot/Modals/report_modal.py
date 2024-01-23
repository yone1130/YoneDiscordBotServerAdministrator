"""

Yone Discord Bot Server Administrator

Copyright (c) よね/Yone

Licensed under the Apache License 2.0.

"""

import discord
from discord import ui

from bot.report import Report

class ReportModal(ui.Modal, title="Report"):
    content = ui.TextInput(label="通報内容", style=discord.TextStyle.paragraph)


    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"通報内容を送信しました。")
        await Report.send(
            user=interaction.user,
            interaction=interaction,
            title="",
            content=self.content,
        )
