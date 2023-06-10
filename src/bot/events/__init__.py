"""

__init__.py | bot/events | Yone Discord Bot Server Administrator

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


class Events:
    def __init__(
        self,
        *,
        client: discord.Client,
        tasks: tasks,
        command_tree: discord.app_commands.CommandTree,
        db_cur: sqlite3.Cursor,
        vc_check: Voice_channel_check,
    ) -> None:
        # ----- On ready ----- #
        @client.event
        async def on_ready():
            await command_tree.sync()
            voice_channel_check.start()
            print(">Ready.  Waiting for any command and message\n")
            return

        # ----- On message ----- #
        @client.event
        async def on_message(message):
            if message.author.bot:
                return

            if message.author.guild_permissions.administrator:
                pass

            else:
                if client.user in message.mentions:
                    await message.reply(
                        embed=discord.Embed(
                            title="Pong", description="Hi", color=0x40FF40
                        )
                    )
                    return

                if len(message.mentions) >= 5:
                    await message.reply(
                        embed=discord.Embed(
                            title="⚠警告⚠",
                            description="大量メンション行為は禁止です。\n"
                            + "該当メッセージは削除されます。\n"
                            + "※この警告メッセージは１５秒後に自動削除します。",
                            color=0xFF4040,
                        ).set_footer(text="警告種別コード: 0x0101"),
                        delete_after=15,
                    )
                    await message.delete()

                    channel = client.get_channel(config.spamChannels[message.guild.id])
                    await channel.send(
                        embed=discord.Embed(
                            title="スパム行為を検出",
                            description="スパム行為 大量メンション を検出したため、\n"
                            + "該当メッセージを削除しました。\n",
                            color=0xFFFF40,
                        )
                        .add_field(name="チャンネル", value=message.channel.mention)
                        .add_field(name="メッセージ送信者", value=message.author.mention)
                        .add_field(name="メッセージ内容", value=f"{message.content}")
                    )

                    return

            return

        # ----- On member join ----- #
        @client.event
        async def on_member_join(member):
            # log
            if member.guild.id in config.joinedChannels:
                embed = discord.Embed(
                    title=f"{member.name} が参加しました。",
                    color=0x40FF40,
                )
                embed.set_thumbnail(url=member.avatar)

                if member.bot:
                    embed.description = "これはBotアカウントです。"

                else:
                    embed.description = f"{member.guild.name} へようこそ！"

                created_at = (
                    str(member.created_at.year)
                    + "/"
                    + str(member.created_at.month).zfill(2)
                    + "/"
                    + str(member.created_at.day).zfill(2)
                    + " "
                    + str(member.created_at.hour).zfill(2)
                    + ":"
                    + str(member.created_at.minute).zfill(2)
                    + ":"
                    + str(member.created_at.second).zfill(2)
                )

                embed.add_field(name="ユーザー名", value=member.mention)
                embed.add_field(name="アカウントの作成日時", value=created_at)
                channel = client.get_channel(config.joinedChannels[member.guild.id])
                await channel.send(embed=embed)

            # global ban
            try:
                db_cur.execute(
                    f"SELECT uid FROM globalBannedList WHERE uid=?", (str(member.id),)
                )
                data = db_cur.fetchall()

            except Exception as e:
                print(f"[ERROR] {e}")
                return

            if data:
                try:
                    await member.ban(reason="グローバルBANリストに登録されているため")

                    try:
                        embed = discord.Embed(
                            title="Global Ban",
                            description=f"{member.name} はグローバルBANリストに登録されているため、BANされました。",
                            color=0x40FF40,
                        )
                        embed.set_thumbnail(url=member.avatar)
                        channel = client.get_channel(
                            config.joinedChannels[member.guild.id]
                        )
                        await channel.send(embed=embed)

                    except:
                        pass

                except Exception as e:
                    try:
                        embed = EmbedOfException(
                            errCode=0x0301,
                            text=f"{member.name} はグローバルBANリストに登録されているため、BANを試みましたが失敗しました。",
                            error=e,
                        )
                        embed.set_thumbnail(url=member.avatar)
                        channel = client.get_channel(
                            config.joinedChannels[member.guild.id]
                        )
                        await channel.send(embed=embed)

                    except:
                        pass

            # welcome
            if member.bot == False:
                if member.guild.id in config.welcomeChannels:
                    channel = client.get_channel(
                        config.welcomeChannels[member.guild.id]
                    )
                    ruleChannel = client.get_channel(
                        config.ruleChannels[member.guild.id]
                    )

                    if member.guild.id in {1053378444781703339}:  # My server
                        await channel.send(
                            content=f"{member.mention} さん。\n\n"
                            + f"ようこそ {member.guild.name} へ！\n"
                            + f"Welcome to {member.guild.name}!\n\n"
                            + "参加いただきありがとうございます。\n"
                            + "Thank you for joining.\n\n"
                            + "必ずガイドラインをご確認ください。\n"
                            + "Please check the guidelines.\n"
                            + f"{ruleChannel.mention}\n\n"
                        )

                    else:  # Other guild
                        await channel.send(
                            content=f"{member.mention} さん。\n\n"
                            + f"ようこそ {member.guild.name} へ！\nWelcome to {member.guild.name}!\n\n"
                            + "必ずルールをご確認ください。\nPlease check the rule.\n"
                            + f"{ruleChannel.mention}"
                        )

            return

        # ----- On member remove ----- #
        @client.event
        async def on_member_remove(member):
            if member.guild.id in config.joinedChannels:
                embed = discord.Embed(
                    title=f"{member.name} が脱退しました。",
                    color=0x40FF40,
                )
                embed.set_thumbnail(url=member.avatar)

                if member.bot == True:
                    embed.description = "これはBotアカウントです。"

                else:
                    embed.description = f"参加ありがとうございました。"

                embed.add_field(name="ユーザー名", value=member.mention)
                channel = client.get_channel(config.joinedChannels[member.guild.id])
                await channel.send(embed=embed)

            return

        # ----- On reaction add ----- #
        @client.event
        async def on_raw_reaction_add(reaction):
            global voice_check_messages

            if reaction.message_id in [
            ]:
                roles = reaction.member.guild.get_role(
                    config.memberRoles[reaction.member.guild.id]
                )
                await reaction.member.add_roles(roles, reason="ガイドラインに同意しました。")

            # Voice channel check message
            for message in list(voice_check_messages.values()):
                if reaction.message_id == message.id:
                    vc_check.add(reaction.member)
                    voice_check_messages.pop(reaction.member.id)
                    await message.edit(content="リアクションを確認しました。")

            return

        # ----- On voice state update ----- #
        @client.event
        async def on_voice_state_update(member, before, after):
            global vc_check
            global voice_check_messages

            if before.channel is None:
                try:
                    db_cur.execute(
                        f"SELECT channelId FROM vcAlertDisableChannels WHERE channelId=?",
                        (str(after.channel.id),),
                    )
                    data = db_cur.fetchall()

                except Exception as e:
                    pass

                if data:
                    pass
                else:
                    vc_check.add(member)

            if after.channel is None:
                vc_check.remove(member)
                voice_check_messages.pop(member.id, None)

        # ----- Tasks ----- #
        @tasks.loop(seconds=480)
        async def voice_channel_check():
            global voice_check_messages
            dt = datetime.datetime.now()

            for vc_data in list(vc_check.check_all()):
                user_attr = vc_data[1][0]
                join_dt = vc_data[1][1]
                td = dt - join_dt

                if (join_dt is not None) and (td.seconds > 14400):
                    channel = client.get_channel(
                        config.voiceAlertChannel[user_attr.guild.id]
                    )

                    if voice_check_messages.get(user_attr.id) is None:
                        msg = await channel.send(
                            content=f"{user_attr.mention} ボイスチャンネルに４時間以上参加しています。\n"
                            + "通話を続ける場合は ✅ をリアクションしてください。\n"
                            + "応答がない場合には10分以内に切断されます。"
                        )
                        await msg.add_reaction("✅")

                        voice_check_messages.update({user_attr.id: msg})

                    else:
                        await user_attr.move_to(None, reason="応答なしのため自動切断しました。")
                        msg = await channel.send(
                            content=f"{user_attr.mention} 応答がないためボイスチャンネルから自動切断されました。"
                        )
