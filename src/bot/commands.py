"""

Yone Discord Bot Server Administrator

Copyright (c) 2022-2024 よね/Yone

Licensed under the Apache License 2.0.

"""

import discord

from bot.report import ReportView
from data import config
from database import BotDatabase
from errors import *
from bot.voice.voice_client import VoiceClient

class Commands:
    def __init__(
        self,
        *,
        client: discord.Client,
        errors: Errors,
        cmdTree: discord.app_commands.CommandTree,
        database: BotDatabase,
    ) -> None:
        self.client = client

        @discord.app_commands.guilds(
            discord.Object(id=config.DISCORD_BOT_DATA["mainGuildId"])
        )
        @cmdTree.command(name="info", description="Send bot information.")
        async def info(inter: discord.Interaction):
            try:
                num_servers = len(client.guilds)

                embed = discord.Embed(
                    title=config.__title__,
                    color=0x40FF40,
                    description=f"{config.__copyright__}\n"
                    + "不具合等の連絡は <@892376684093898772> までお願いいたします。",
                ).add_field(name="■導入サーバー数", value=num_servers)

                await inter.response.send_message(embed=embed)
                return

            except Exception as error:
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
                return

        @cmdTree.command(name="clear", description="Delete message(s).")
        @discord.app_commands.describe(target="削除するメッセージ数")
        async def clear(inter: discord.Interaction, target: int):
            try:
                if inter.user.guild_permissions.administrator:
                    await inter.response.send_message(content="Please wait while...")

                    purge_limit = target + 1

                    deleted = await inter.channel.purge(
                        limit=purge_limit, reason=f"{inter.user.name} が /clear を使用しました。"
                    )

                    num_of_deleted = len(deleted)

                    result_embed = discord.Embed(
                        title="Deleted messages",
                        color=0x40FF40,
                        description=f"{num_of_deleted}個のメッセージを削除しました。\n"
                        + f"{inter.user.mention} が /clear を使用しました。",
                    )

                    await inter.channel.send(
                        embed=result_embed,
                        delete_after=10,
                    )

                    return

                else:
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="あなたはこのコマンドを実行する権限がありません。\nYou are not authorized to use this command.",
                    )

                    await inter.response.send_message(
                        embed=embed,
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
                return

        @cmdTree.command(
            name="guilds", description="Send number of this bot joining servers."
        )
        async def guilds(inter: discord.Interaction):
            try:
                num_servers = len(client.guilds)
                embed = discord.Embed(
                    title=f"{config.__title__}",
                    description=f"導入サーバー数: {num_servers}\n",
                    color=0x40F040,
                )

                for guild in client.guilds:
                    embed.description = (
                        embed.description
                        + f"\n- {guild.name}\nオーナー: {guild.owner.mention} ({guild.owner.name})"
                    )

                await inter.response.send_message(embed=embed)

                return

            except Exception as error:
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
                return

        @cmdTree.command(name="gban-add", description="User add to global banned list.")
        @discord.app_commands.describe(target="追加するユーザー")
        async def gban_add(inter: discord.Interaction, target: discord.Member):
            import datetime

            try:
                if inter.user.guild_permissions.administrator:
                    try:
                        data = database.get_gban(target=target.id)

                    except Exception as error:
                        errors.exception_log_message_send(error=error)

                        embed = errors.embed_of_exception(
                            err_code=0x0202, text="データベースの読み込みに失敗しました。", error=error
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )

                        return

                    if (not data) or (data is None):
                        dt_Now = datetime.datetime.now()
                        dt_str = dt_Now.strftime("%Y%m%d%H%M%S")

                        embed_of_result = discord.Embed(
                            title="Global Ban",
                            color=0x40FF40,
                            description=f"{target.mention} をGlobal Bannedリストに登録しました。",
                        )

                        database.insert_gban(target=target.id, add_datetime=dt_str)

                        await inter.response.send_message(
                            embed=embed_of_result,
                            ephemeral=True,
                        )
                        return

                    else:
                        embed = discord.Embed(
                            title="Global Ban",
                            color=0xFF4040,
                            description="このユーザーはすでにGlobal Bannedリストに登録されています。",
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )
                        return

                else:
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="あなたはこのコマンドを実行する権限がありません。",
                    )

                    await inter.response.send_message(
                        embed=embed,
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
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
                        errors.exception_log_message_send(error=error)

                        embed = errors.embed_of_exception(
                            err_code=0x0202, text="データベースの読み込みに失敗しました。", error=error
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )

                        return

                    if data:
                        database.delete_gban_user(target=target)

                        embed = discord.Embed(
                            title="Global Ban",
                            color=0x40FF40,
                            description=f"<@{target}> をGlobal Bannedリストから削除しました。",
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )

                        return

                    else:
                        embed = discord.Embed(
                            title="Global Ban",
                            color=0xFF4040,
                            description="このユーザーIDはGlobal Bannedリストに登録されていません。",
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )
                        return

                else:
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="あなたはこのコマンドを実行する権限がありません。",
                    )

                    await inter.response.send_message(
                        embed=embed,
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
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
                        errors.exception_log_message_send(error=errors)

                        embed = errors.embed_of_exception(
                            err_code=0x0202, text="データベースの読み込みに失敗しました。", error=error
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )

                        return

                    if (not data) or (data is None):
                        database.insert_vc_alert_disable_channels(target=target.id)

                        embed = discord.Embed(
                            title="Voice channel long time alert",
                            color=0x40FF40,
                            description=f"{target.mention} では、長時間の通話による自動切断を無効にしました。",
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )

                        return

                    else:
                        embed = discord.Embed(
                            title="Voice channel long time alert",
                            color=0xFF4040,
                            description="このチャンネルではすでに、長時間の通話による自動切断が無効化されています。",
                        )

                        await inter.response.send_message(
                            embed=embed,
                            ephemeral=True,
                        )
                        return

                else:
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="このコマンドはサーバー管理者のみ実行できます。",
                    )

                    await inter.response.send_message(
                        embed=embed,
                        ephemeral=True,
                    )
                    return

            except Exception as error:
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
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
                        errors.exception_log_message_send(error=errors)
                        await inter.response.send_message(
                            embed=errors.embed_of_exception(
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
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)

                await inter.response.send_message(embed=embed, ephemeral=False)
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
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
                return

        @cmdTree.command(name="join", description="Join voice channel.")
        async def join(inter: discord.Interaction, channel: discord.VoiceChannel):
            try:
                voice_client = channel.connect(cls=VoiceClient)

            except Exception as error:
                errors.exception_log_message_send(error=error)

                embed = errors.embed_of_unhandled_exception(error=error)
                await inter.response.send_message(embed=embed, ephemeral=False)
                return
