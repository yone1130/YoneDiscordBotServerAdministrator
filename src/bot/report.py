"""

report.py | bot | Yone Discord Bot Server Administrator

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord
from data import config


class Report:
    SELECTS = {
        'text': "通報内容を自分で入力する",
        'user-spam': "スパム行為を行っているユーザーを発見した",
        'user-troll': "荒らし行為を行っているユーザーを発見した",
        'user-sus': "何かあったわけではないが、不審なユーザーがいる",
    }

    async def __init__(self) -> None:
        pass
    
    async def send(
        *,
        user: discord.User,
        interaction: discord.Interaction,
        title: str,
        content: str
    ) -> None:
        embed = EmbedOfReceiveReport.embed(
            user=user,
            title=title,
            content=content
        )

        await interaction.client.get_channel(config.REPORT_POST_CHANNEL).send(
            content=f"<@{config.OWNER_USER_ID}>",
            embed=embed
        )


class ReportView:
    def __init__(self) -> None:
        pass

    def make_view() -> discord.ui.View:
        view = discord.ui.View(timeout=120).add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.red,
                label="通報内容を送信する",
                custom_id="btn_report_submit"
            )
        ).add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.gray,
                label="終了",
                custom_id="btn_report_exit",
            )
        ).add_item(
            discord.ui.Select(
                custom_id="select_report_type",
                options=[
                    discord.SelectOption(
                        label="通報内容を自分で入力する",
                        value='text'
                    ),
                    discord.SelectOption(
                        label="スパム行為を行っているユーザーを発見した",
                        value='user-spam'
                    ),
                    discord.SelectOption(
                        label="荒らし行為を行っているユーザーを発見した",
                        value='user-troll'
                    ),
                    discord.SelectOption(
                        label="何かあったわけではないが、不審なユーザーがいる",
                        value='user-sus'
                    ),
                ]
            )
        )
        return view


class EmbedOfReceiveReport:
    def __init__(self) -> None:
        pass

    def embed(
        *,
        user: discord.User,
        title: str,
        content: str
    ) -> discord.Embed:
        embed = discord.Embed(
            title="通報",
            description="ユーザーからの通報を受け取りました。",
            color=0xf04040
        ).add_field(
            name="■ 通報者 (ユーザーID)",
            value=f"{user.mention} ({user.name})"
        ).add_field(
            name="■ 通報件名",
            value=title
        ).add_field(
            name="通報内容",
            value=content
        )
        return embed