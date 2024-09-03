"""

Yone Discord Bot Server Administrator

Copyright (C) よね/Yone

Licensed under the Apache License 2.0.

"""

import datetime

import discord
from discord.ext import tasks

from bot.report import Report, ReportView
from data import config
from database import BotDatabase
from errors import *
from voice_channel_check import Voice_channel_check

from .Modals.report_modal import ReportModal


class Events:
    def __init__(
        self,
        *,
        client: discord.Client,
        errors: Errors,
        tasks: tasks,
        command_tree: discord.app_commands.CommandTree,
        database: BotDatabase,
        vc_check: Voice_channel_check,
        voice_check_messages: dict,
    ) -> None:
        self.client = client
        self.report_type_value = ""
        self.report_user_value = ""
        self.duplicate_message_count = {}
        self.message_content_last = ""

        @client.event
        async def on_ready():
            print("[INFO] Logged in.")
            commands = await command_tree.sync()
            print(f"[INFO] {len(commands)} command(s) has synced.")
            voice_channel_check.start()
            print("[INFO] Ready.")
            return

        @client.event
        async def on_message(message: discord.Message):
            if message.author.bot:
                return

            else:
                num_mentions = len(message.mentions)

                channel_log = self.duplicate_message_count.get(
                    str(message.channel.id), {}
                )
                if channel_log == {}:
                    self.duplicate_message_count[str(message.channel.id)] = {
                        "count": 0,
                        "user": message.author.id,
                    }

                if (
                    message.content == self.message_content_last
                    and message.author.id
                    == self.duplicate_message_count[str(message.channel.id)]["user"]
                ):
                    self.duplicate_message_count[str(message.channel.id)]["count"] = (
                        self.duplicate_message_count[str(message.channel.id)]["count"]
                        + 1
                    )
                else:
                    self.duplicate_message_count[str(message.channel.id)]["count"] = 0

                self.duplicate_message_count[str(message.channel.id)] = {
                    "count": self.duplicate_message_count[str(message.channel.id)][
                        "count"
                    ],
                    "user": message.author.id,
                }

                if self.duplicate_message_count[str(message.channel.id)]["count"] >= 5:
                    embed = discord.Embed(
                        title="⚠警告⚠",
                        description="重複した内容を連続して送信する行為は禁止です。\n"
                        + "該当メッセージは削除されます。\n"
                        + "措置: タイムアウト1分",
                        color=0xFF4040,
                    ).set_footer(text="警告種別コード: 2")

                    await message.reply(
                        embed=embed,
                        delete_after=15,
                    )
                    await message.delete()

                    until = datetime.timedelta(seconds=60)
                    await message.author.timeout(
                        until, reason="スパム行為: 重複した内容の連投"
                    )

                self.message_content_last = message.content

                if num_mentions >= 5 and (
                    not message.author.guild_permissions.administrator
                ):
                    log_channel = client.get_channel(
                        config.spamChannels[message.guild.id]
                    )

                    embed = discord.Embed(
                        title="⚠警告⚠",
                        description="大量メンション行為は禁止です。\n"
                        + "該当メッセージは削除されます。\n",
                        color=0xFF4040,
                    ).set_footer(text="警告種別コード: 1")

                    embed_of_log = (
                        discord.Embed(
                            title="スパム行為を検出",
                            description="スパム行為 大量メンション を検出したため、\n"
                            + "該当メッセージを削除しました。\n",
                            color=0xFFFF40,
                        )
                        .add_field(name="チャンネル", value=message.channel.mention)
                        .add_field(
                            name="メッセージ送信者", value=message.author.mention
                        )
                        .add_field(name="メッセージ内容", value=f"{message.content}")
                    )

                    await message.reply(
                        embed=embed,
                        delete_after=15,
                    )
                    await message.delete()
                    await log_channel.send(embed=embed_of_log)

                    return

                if client.user in message.mentions:
                    await message.reply(
                        content="サポートが必要な場合はプロフィールにある招待リンクからサポートサーバーへ参加してください。/info コマンドを使用して、このBotの情報を表示します。\n"
                        + "Hi. Do you need help? You can join this bot's support server. Please check the invite link on my profile. And type the /info command to see information about this bot."
                    )
                    return

            return

        @client.event
        async def on_member_join(member):
            # log
            if member.guild.id in config.joinedChannels:
                embed = (
                    discord.Embed(
                        title=f"{member.name} が参加しました。",
                        color=0x40FF40,
                    )
                    .add_field(name="ユーザー名", value=member.mention)
                    .set_thumbnail(url=member.avatar)
                )

                if member.bot:
                    embed.description = "これはBotアカウントです。"
                else:
                    embed.description = f"{member.guild.name} へようこそ！"

                account_created_at_year = str(member.created_at.year)
                account_created_at_month = str(member.created_at.month)
                account_created_at_day = str(member.created_at.day)
                account_created_at_hour = str(member.created_at.hour)
                account_created_at_minute = str(member.created_at.minute)
                account_created_at_second = str(member.created_at.second)

                created_at = (
                    f"{account_created_at_year}/{account_created_at_month}/{account_created_at_day}"
                    + f"{account_created_at_hour}:{account_created_at_minute}:{account_created_at_second}"
                )

                embed.add_field(name="アカウントの作成日時", value=created_at)
                channel = client.get_channel(config.joinedChannels[member.guild.id])
                await channel.send(embed=embed)

            # global ban
            try:
                data = database.get_gban(target=member.id)

            except Exception as error:
                errors.exception(error=error)
                return

            if data:
                try:
                    await member.ban(reason="グローバルBANリストに登録されているため")

                    try:
                        embed = discord.Embed(
                            title="Global Ban",
                            description=f"{member.name} はグローバルBANリストに登録されているため、BANされました。",
                            color=0x40FF40,
                        ).set_thumbnail(url=member.avatar)

                        channel = client.get_channel(
                            config.joinedChannels[member.guild.id]
                        )

                        await channel.send(embed=embed)
                        return

                    except Exception as error:
                        errors.exception(error=error)
                        return

                except Exception as error:
                    try:
                        embed = errors.embed_of_exception(
                            err_code=0x0301,
                            text=f"{member.name} はグローバルBANリストに登録されているため、BANを試みましたが失敗しました。",
                            error=error,
                        ).set_thumbnail(url=member.avatar)

                        channel = client.get_channel(
                            config.joinedChannels[member.guild.id]
                        )
                        await channel.send(embed=embed)

                    except Exception as error:
                        errors.exception(error=error)

            # welcome
            if member.bot == False:
                if member.guild.id in config.welcomeChannels:
                    channel = client.get_channel(
                        config.welcomeChannels[member.guild.id]
                    )
                    ruleChannel = client.get_channel(
                        config.ruleChannels[member.guild.id]
                    )

                    guilds = {1053378444781703339}
                    if member.guild.id in guilds:  # My server
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

        @client.event
        async def on_member_remove(member):
            if member.guild.id in config.joinedChannels:
                embed = (
                    discord.Embed(
                        title=f"{member.name} が脱退しました。",
                        color=0x40FF40,
                    )
                    .set_thumbnail(url=member.avatar)
                    .add_field(name="ユーザー名", value=member.mention)
                )
                if member.bot == True:
                    embed.description = "これはBotアカウントです。"
                else:
                    embed.description = f"参加ありがとうございました。"

                channel = client.get_channel(config.joinedChannels[member.guild.id])
                await channel.send(embed=embed)

            return

        @client.event
        async def on_raw_reaction_add(reaction):
            id_of_messages = [
                1074994444509642752,
                1073629279079911505,
                1055443071866765352,
                1083296365381169214,
                1117249215215718472,
            ]

            if reaction.message_id in id_of_messages:
                roles = reaction.member.guild.get_role(
                    config.memberRoles[reaction.member.guild.id]
                )
                await reaction.member.add_roles(
                    roles, reason="ガイドラインに同意しました。"
                )

            # Voice channel check message
            messages_of_vc_check = list(voice_check_messages.values())

            for message in messages_of_vc_check:
                if reaction.message_id == message.id:
                    vc_check.add(reaction.member)
                    voice_check_messages.pop(reaction.member.id)
                    await message.edit(content="リアクションを確認しました。")

            return

        @client.event
        async def on_voice_state_update(member, before, after):
            if before.channel is None:
                if member.bot:
                    return

                try:
                    data = database.get_vc_alert_disable_channels(
                        target=after.channel.id
                    )

                except Exception as error:
                    errors.exception(error=error)
                    return

                if data:
                    pass
                else:
                    vc_check.add(member)

                return

            if after.channel is None:
                vc_check.remove(member)
                voice_check_messages.pop(member.id, None)
                return

        @client.event
        async def on_interaction(inter: discord.Interaction):
            component_type = inter.data.get("component_type")

            if component_type == int(discord.ComponentType.button):
                await self.on_click_button(interaction=inter)

            elif component_type == int(discord.ComponentType.select):
                await self.on_change_select(interaction=inter)

            elif component_type == int(discord.ComponentType.user_select):
                await self.on_change_user_select(interaction=inter)

            else:
                return

        @tasks.loop(seconds=600)
        async def voice_channel_check():
            dt = datetime.datetime.now()

            for vc_data in list(vc_check.check_all()):
                user_attr = vc_data[1][0]
                join_dt = vc_data[1][1]
                td = dt - join_dt

                if (join_dt is not None) and (td.seconds > 21600):
                    channel = client.get_channel(
                        config.voiceAlertChannel[user_attr.guild.id]
                    )

                    if voice_check_messages.get(user_attr.id) is None:
                        msg = await channel.send(
                            content=f"{user_attr.mention} ボイスチャンネルに6時間以上参加しています。\n"
                            + "通話を続ける場合は ✅ をリアクションしてください。\n"
                            + "応答がない場合には10分以内に切断されます。"
                        )
                        await msg.add_reaction("✅")

                        voice_check_messages.update({user_attr.id: msg})

                    else:
                        await user_attr.move_to(
                            None, reason="応答なしのため自動切断しました。"
                        )
                        msg = await channel.send(
                            content=f"{user_attr.mention} 応答がないためボイスチャンネルから自動切断されました。"
                        )

    async def on_click_button(self, *, interaction: discord.Interaction) -> None:
        SELECTS = Report.SELECTS
        id = interaction.data.get("custom_id")
        value = self.report_type_value
        user = self.report_user_value

        if id == "btn_report_submit":
            if value == "text":
                modal = ReportModal()
                await interaction.response.send_modal(modal=modal)
                return
            else:
                if value == "":
                    await interaction.response.send_message(
                        content="通報する項目を選択してください。", ephemeral=True
                    )
                    return

                if user == "":
                    await interaction.response.send_message(
                        content="通報するユーザーを選択してください。", ephemeral=True
                    )
                    return

                await Report.send(
                    user=interaction.user,
                    interaction=interaction,
                    title=SELECTS[value],
                    content=f"{user.mention} ({user.name})",
                )
                await interaction.response.send_message(
                    content="通報内容を送信しました。"
                )
                self.report_type_value = ""
                self.report_user_value = ""
                return

        elif id == "btn_report_exit":
            await interaction.response.send_message(
                content="通報セッションを終了しました。", delete_after=3
            )
            await interaction.message.delete()
            self.report_type_value = ""
            self.report_user_value = ""
            return

    async def on_change_select(self, *, interaction: discord.Interaction) -> None:
        SELECTS = Report.SELECTS
        id = interaction.data.get("custom_id")

        if id == "select_report_type":
            self.report_type_value = interaction.data.get("values")[0]
            embed = interaction.message.embeds[0]
            name = embed.fields[0].name
            embed.set_field_at(
                index=0, name=name, value=SELECTS.get(self.report_type_value, None)
            )
            await interaction.response.edit_message(embed=embed)

            view_items = discord.ui.UserSelect(
                custom_id="userslect_report", placeholder="ユーザーを選択"
            )
            view = ReportView.make_view().add_item(item=view_items)

            if self.report_type_value != "text":
                await interaction.message.edit(view=view)

    async def on_change_user_select(self, *, interaction: discord.Interaction) -> None:
        id = interaction.data.get("custom_id")

        if id == "userslect_report":
            user = interaction.data.get("values")[0]
            self.report_user_value = self.client.get_user(int(user))
            embed = interaction.message.embeds[0]
            name = embed.fields[1].name

            embed.set_field_at(index=1, name=name, value=self.report_user_value.mention)

            await interaction.response.edit_message(embed=embed)
