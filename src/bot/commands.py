"""

commands.py | bot | Yone Discord Bot Server Administrator

Copyright 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord

from bot.report import ReportView
from data import config
from database import BotDatabase
from errors import *


class Commands:
    def __init__(
        self,
        *,
        client: discord.Client,
        cmdTree: discord.app_commands.CommandTree,
        database: BotDatabase,
    ) -> None:
        self.client = client

        @discord.app_commands.guilds(discord.Object(id=config.MAIN_GUILD_ID))
        @cmdTree.command(name="info", description="Send bot information")
        async def info(inter: discord.Interaction):
            try:
                embed = discord.Embed(
                    title=config.__title__,
                    color=0x40FF40,
                    description=f"{config.__copyright__}\n"
                    + "不具合等の連絡は <@892376684093898772> までお願いいたします。",
                ).add_field(
                    name="■導入サーバー数",
                    value=len(client.guilds)
                )
                await inter.response.send_message(embed=embed)
                return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        @cmdTree.command(name="clear", description="Delete message(s)")
        @discord.app_commands.describe(target="削除するメッセージ数")
        async def clear(inter: discord.Interaction, target: int):
            try:
                if inter.user.guild_permissions.administrator:
                    await inter.response.send_message(content="Please wait while...")

                    deleted = await inter.channel.purge(
                        limit=target + 1, reason=f"{inter.user.name} が /clear を使用しました。"
                    )

                    await inter.channel.send(
                        embed=discord.Embed(
                            title="Deleted messages",
                            color=0x40FF40,
                            description=f"{len(deleted)-1}個のメッセージを削除しました。\n"
                            + f"{inter.user.mention} が /clear を使用しました。",
                        ),
                        delete_after=10,
                    )

                    return

                else:
                    await inter.response.send_message(
                        embed=discord.Embed(
                            title="Error",
                            color=0xFF4040,
                            description="あなたはこのコマンドを実行する権限がありません。",
                        ),
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        @cmdTree.command(name="gban-add", description="User add to global banned list.")
        async def gban_add(inter: discord.Interaction, target: discord.Member):
            import datetime

            try:
                if inter.user.guild_permissions.administrator:
                    try:
                        data = database.get_gban(target=target.id)

                    except Exception as error:
                        await inter.response.send_message(
                            embed=EmbedOfException(
                                err_code=0x0202, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if (not data) or (data is None):
                        dt_Now = datetime.datetime.now()
                        datetime = dt_Now.strftime("%Y%m%d%H%M%S")

                        database.insert_gban(target=target.id, add_datetime=datetime)

                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Global Ban",
                                color=0x40FF40,
                                description=f"{target.mention} をGlobal Bannedリストに登録しました。",
                            ),
                            ephemeral=True,
                        )
                        return

                    else:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Global Ban",
                                color=0xFF4040,
                                description="このユーザーはすでにGlobal Bannedリストに登録されています。",
                            ),
                            ephemeral=True,
                        )
                        return

                else:
                    await inter.response.send_message(
                        embed=discord.Embed(
                            title="Error",
                            color=0xFF4040,
                            description="あなたはこのコマンドを実行する権限がありません。",
                        ),
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        @cmdTree.command(
            name="gban-rmv", description="User remove from global banned list."
        )
        @discord.app_commands.describe(target="リストから削除するユーザーのID")
        async def gban_rmv(inter: discord.Interaction, target: str):
            try:
                if inter.user.guild_permissions.administrator:
                    try:
                        data = database.get_gban(target=target)

                    except Exception as error:
                        await inter.response.send_message(
                            embed=EmbedOfException(
                                err_code=0x0202, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if data:
                        database.delete_gban_user(target=target)

                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Global Ban",
                                color=0x40FF40,
                                description=f"<@{target}> をGlobal Bannedリストから削除しました。",
                            ),
                            ephemeral=True,
                        )
                        return

                    else:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Global Ban",
                                color=0xFF4040,
                                description="このユーザーIDはGlobal Bannedリストに登録されていません。",
                            ),
                            ephemeral=True,
                        )
                        return

                else:
                    await inter.response.send_message(
                        embed=discord.Embed(
                            title="Error",
                            color=0xFF4040,
                            description="あなたはこのコマンドを実行する権限がありません。",
                        ),
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        @cmdTree.command(
            name="vc-alert-disable",
            description="Voice channel long time alert to disable.",
        )
        async def vc_alert_disable(
            inter: discord.Interaction, target: discord.VoiceChannel
        ):
            try:
                if inter.user.guild_permissions.administrator:
                    try:
                        data = database.get_vc_alert_disable_channels(target=target.id)

                    except Exception as error:
                        await inter.response.send_message(
                            embed=EmbedOfException(
                                err_code=0x0202, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if (not data) or (data is None):
                        database.insert_vc_alert_disable_channels(target=target.id)

                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Voice channel long time alert",
                                color=0x40FF40,
                                description=f"{target.mention} では、長時間の通話による自動切断を無効にしました。",
                            ),
                            ephemeral=True,
                        )
                        return

                    else:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Voice channel long time alert",
                                color=0xFF4040,
                                description="このチャンネルではすでに、長時間の通話による自動切断が無効化されています。",
                            ),
                            ephemeral=True,
                        )
                        return

                else:
                    await inter.response.send_message(
                        embed=discord.Embed(
                            title="Error",
                            color=0xFF4040,
                            description="このコマンドはサーバー管理者のみ実行できます。",
                        ),
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        @cmdTree.command(
            name="vc-alert-enable",
            description="Voice channel long time alert to enable.",
        )
        async def vc_alert_enable(
            inter: discord.Interaction, target: discord.VoiceChannel
        ):
            try:
                if inter.user.guild_permissions.administrator:
                    try:
                        data = database.get_vc_alert_disable_channels(target=target.id)

                    except Exception as error:
                        await inter.response.send_message(
                            embed=EmbedOfException(
                                err_code=0x0202, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if data:
                        database.delete_vc_alert_disable_channels(target=target.id)

                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Voice channel long time alert",
                                color=0x40FF40,
                                description=f"{target.mention} では、長時間の通話による自動切断を有効にしました。",
                            ),
                            ephemeral=True,
                        )
                        return

                    else:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="Voice channel long time alert",
                                color=0xFF4040,
                                description="このチャンネルではすでに、長時間の通話による自動切断が有効化されています。",
                            ),
                            ephemeral=True,
                        )
                        return

                else:
                    await inter.response.send_message(
                        embed=discord.Embed(
                            title="Error",
                            color=0xFF4040,
                            description="このコマンドはサーバー管理者のみ実行できます。",
                        ),
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        @cmdTree.command(name="report", description="Report anything.")
        async def report(inter: discord.Interaction):
            try:
                await inter.response.send_message(
                    embed=discord.Embed(
                        title="Yone 荒らし対策サポート - レイド通報",
                        description="Yone 荒らし対策サポートへ レイドを通報します。",
                    )
                    .add_field(name="選択した項目:", value="**選択してください**")
                    .add_field(name="選択した項目2:", value="-"),
                    view=ReportView.make_view(),
                )
                return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return
