"""

__init__.py | bot/commands | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import datetime
import sqlite3
import discord
from discord.ext import tasks

try:
    from data import config
    from errors import *
    from voice_channel_check import Voice_channel_check
except ModuleNotFoundError as error:
    print(f"[ERROR] {error}")


class Commands:
    def __init__(
        self,
        *,
        client: discord.Client,
        tasks: tasks,
        cmdTree: discord.app_commands.CommandTree,
        vc_check: Voice_channel_check,
        db_con: sqlite3.Connection,
        db_cur: sqlite3.Cursor,
    ) -> None:
        @discord.app_commands.guilds(discord.Object(id=0))

        # ----- info ----- #
        @cmdTree.command(name="info", description="Send bot information")
        async def info(inter: discord.Interaction):
            try:
                embed = discord.Embed(
                    title="Yone Bot Server Administrator",
                    color=0x40FF40,
                    description="(c) 2022-2023 よね/Yone\n"
                    + "不具合等の連絡は <@892376684093898772> までお願いいたします。",
                )
                await inter.response.send_message(embed=embed)
                return

            except Exception as error:
                UnhandledException(error)
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
                UnhandledException(error)
                return

        # ----- global ban add ----- #
        @cmdTree.command(name="gban-add", description="User add to global banned list.")
        async def gban_add(inter: discord.Interaction, target: discord.Member):
            try:
                if inter.user.guild_permissions.administrator:
                    try:
                        db_cur.execute(
                            f"SELECT uid, datetime FROM globalBannedList WHERE uid=?",
                            (str(target.id),),
                        )
                        data = db_cur.fetchall()

                    except Exception as e:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="エラーが発生しました",
                                color=0xFF4040,
                                description=f"データベースの読み込みに失敗しました。```{e}```",
                            ).set_footer(text=f"エラーコード: 0x0201"),
                            ephemeral=True,
                        )
                        return

                    if (not data) or (data is None):
                        dt_Now = datetime.datetime.now()
                        add_datetime = dt_Now.strftime("%Y%m%d%H%M%S")

                        insertData = (str(target.id), add_datetime)
                        db_cur.execute(
                            "INSERT INTO globalBannedList VALUES(?, ?)", insertData
                        )
                        db_con.commit()

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
                UnhandledException(error)
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
                        db_cur.execute(
                            f"SELECT uid FROM globalBannedList WHERE uid=?", (target,)
                        )
                        data = db_cur.fetchall()

                    except Exception as e:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="エラーが発生しました",
                                color=0xFF4040,
                                description=f"データベースの読み込みに失敗しました。```{e}```",
                            ).set_footer(text=f"エラーコード: 0x0201"),
                            ephemeral=True,
                        )
                        return

                    if data:
                        db_cur.execute(
                            "DELETE FROM globalBannedList WHERE uid=?", (target,)
                        )
                        db_con.commit()

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
                UnhandledException(error)
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
                        db_cur.execute(
                            f"SELECT channelId FROM vcAlertDisableChannels WHERE channelId=?",
                            (str(target.id),),
                        )
                        data = db_cur.fetchall()

                    except Exception as e:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="エラーが発生しました",
                                color=0xFF4040,
                                description=f"データベースの読み込みに失敗しました。```{e}```",
                            ).set_footer(text=f"エラーコード: 0x0201"),
                            ephemeral=True,
                        )
                        return

                    if (not data) or (data is None):
                        insertData = (str(target.id),)
                        db_cur.execute(
                            "INSERT INTO vcAlertDisableChannels VALUES(?)", insertData
                        )
                        db_con.commit()

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
                UnhandledException(error)
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
                        db_cur.execute(
                            f"SELECT channelId FROM vcAlertDisableChannels WHERE channelId=?",
                            (str(target.id),),
                        )
                        data = db_cur.fetchall()

                    except Exception as e:
                        await inter.response.send_message(
                            embed=discord.Embed(
                                title="エラーが発生しました",
                                color=0xFF4040,
                                description=f"データベースの読み込みに失敗しました。```{e}```",
                            ).set_footer(text=f"エラーコード: 0x0201"),
                            ephemeral=True,
                        )
                        return

                    if data:
                        db_cur.execute(
                            "DELETE FROM vcAlertDisableChannels WHERE channelId=?",
                            (str(target.id),),
                        )
                        db_con.commit()

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
                UnhandledException(error)
                return
