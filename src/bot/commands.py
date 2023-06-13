"""

__init__.py | bot/commands | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord
from discord.ext import tasks

from data import config
from database import BotDatabase
from errors import *
from voice_channel_check import Voice_channel_check


class Commands:
    def __init__(
        self,
        *,
        client: discord.Client,
        tasks: tasks,
        cmdTree: discord.app_commands.CommandTree,
        database: BotDatabase,
        vc_check: Voice_channel_check,
    ) -> None:
        @discord.app_commands.guilds(discord.Object(id=config.MAIN_GUILD_ID))

        # ----- info ----- #
        @cmdTree.command(name="info", description="Send bot information")
        async def info(inter: discord.Interaction):
            try:
                embed = discord.Embed(
                    title=config.__title__,
                    color=0x40FF40,
                    description=f"{config.__copyright__}\n"
                    + "不具合等の連絡は <@892376684093898772> までお願いいたします。",
                )
                await inter.response.send_message(embed=embed)
                return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        # ----- clear ----- #
        @cmdTree.command(name="clear", description="Clear message(s)")
        async def clear(inter: discord.Interaction, target: int):
            try:
                if inter.user.guild_permissions.administrator:
                    await inter.response.send_message(content="Please while...")

                    deleted = await inter.channel.purge(
                        limit=target + 1, reason=f"{inter.user.name} が /clear を使用しました。"
                    )

                    embed = discord.Embed(
                        title="Deleted messages",
                        color=0x40FF40,
                        description=f"{len(deleted)-1}個のメッセージを削除しました。\n"
                        + f"{inter.user.mention} が /clear を使用しました。",
                    )

                    await inter.channel.send(embed=embed, delete_after=10)

                    return

                else:
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="あなたはこのコマンドを実行する権限がありません。",
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        # ----- global ban add ----- #
        @cmdTree.command(name="gban-add", description="User add to global banned list.")
        async def gban_add(inter: discord.Interaction, target: discord.Member):
            try:
                if inter.user.guild_permissions.administrator:
                    try:
                        data = database.get_gban(target=target.id)

                    except Exception as error:
                        await inter.response.send_message(
                            embed=EmbedOfException(
                                err_code=0x0201, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if (not data) or (data is None):
                        dt_Now = datetime.datetime.now()
                        datetime = dt_Now.strftime("%Y%m%d%H%M%S")

                        database.insert_gban(
                            target_id=target.id, add_datetime=datetime
                        )

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
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="あなたはこのコマンドを実行する権限がありません。",
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        # ----- global ban remove ----- #
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
                                err_code=0x0201, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if data:
                        database.delete_gban_user(target_id=target)

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
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="あなたはこのコマンドを実行する権限がありません。",
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        # ----- Voice channel alert invalid add  ----- #
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
                        data = database.get_vc_alert_disable_channels(
                            target_id=target.id
                        )

                    except Exception as error:
                        await inter.response.send_message(
                            embed=EmbedOfException(
                                err_code=0x0201, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if (not data) or (data is None):
                        database.insert_vc_alert_disable_channels(
                            target_id=target.id
                        )

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
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="このコマンドはサーバー管理者のみ実行できます。",
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return

        # ----- Voice channel alert invalid remove ----- #
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
                        data = database.get_vc_alert_disable_channels(
                            target_id=target.id
                        )

                    except Exception as error:
                        await inter.response.send_message(
                            embed=EmbedOfException(
                                err_code=0x0201, text="データベースの読み込みに失敗しました。", error=error
                            ),
                            ephemeral=True,
                        )
                        return

                    if data:
                        database.delete_vc_alert_disable_channels(
                            target_id=target.id
                        )

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
                    embed = discord.Embed(
                        title="Error",
                        color=0xFF4040,
                        description="このコマンドはサーバー管理者のみ実行できます。",
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return

            except Exception as error:
                await inter.response.send_message(
                    embed=EmbedOfUnhandledException(error=error), ephemeral=False
                )
                return
