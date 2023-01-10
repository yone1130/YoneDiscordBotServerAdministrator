#
# YoneDiscordBotServerAdministrator.py | Yone Discord Bot Server Administrator
#
# (c) 2022-2023 よね/Yone
#

import discord


class discordBot(discord.Client):
    async def on_ready(self):
        print(">Ready.  Waiting for any command and message\n")
        return


    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.guild_permissions.administrator:
            pass

        else:
            if len(message.mentions) >= 2:
                await message.reply(
                    embed=discord.Embed(
                        title="警告",
                        description="大量メンション行為は禁止です。\n"+
                                    "該当メッセージは削除されます。\n"+
                                    "※この警告メッセージは１０秒後に自動削除します。",
                        color=0xff4040
                    )
                    .set_footer(
                        text="警告種別コード: 0x01001"
                    ),
                    delete_after=10
                )
                await message.delete()

                channel = discord.Client.get_channel(self, 1062270394482053160)
                await channel.send(
                    embed=discord.Embed(
                        title="__**（これはテストです）**__ スパム行為を検出",
                        description="スパム行為 大量メンション を検出したため、\n"+
                                    "該当メッセージを削除しました。\n",
                        color=0xffff40
                    )
                    .add_field(
                        name="チャンネル",
                        value=message.channel.mention
                    )
                    .add_field(
                        name="メッセージ送信者",
                        value=message.author.mention
                    )
                    .add_field(
                        name="メッセージ内容",
                        value=f"{message.content}"
                    )
                )

                return

        return


    async def on_member_join(self, member):
        embed=discord.Embed(
            title=f"{member.mention} が参加しました。",
            color= 0x40ff40,
        )
        embed.set_thumbnail(url=member.avatar)

        if member.bot == True:
            embed.description = "これはBotアカウントです。"
        else:
            embed.description = f"{member.guild.name} へようこそ！"

        created_at = str(member.created_at.year)+"/"+\
                    str(member.created_at.month).zfill(2)+"/"+\
                    str(member.created_at.day).zfill(2)+" "+\
                    str(member.created_at.hour).zfill(2)+":"+\
                    str(member.created_at.minute).zfill(2)+":"+\
                    str(member.created_at.second).zfill(2)

        embed.add_field(
            name="ユーザー名",
            value=member.name
        )
        embed.add_field(
            name="アカウントの作成日時",
            value=created_at
        )

        channel = discord.Client.get_channel(self, 1053378446627188779)
        await channel.send(embed=embed)

        return


    async def on_member_remove(self, member):
        embed=discord.Embed(
            title=f"{member.mention} が脱退しました。",
            color= 0x40ff40,
        )
        embed.set_thumbnail(url=member.avatar)

        if member.bot == True:
            embed.description = "これはBotアカウントです。"
        else:
            embed.description = f"参加ありがとうございました。"
        
        embed.add_field(
            name="ユーザー名",
            value=member.name
        )

        channel = discord.Client.get_channel(self, 1053378446627188779)
        await channel.send(embed=embed)

        return


    async def on_member_remove(self, member):
        embed=discord.Embed(
            title=f"{member.mention} が脱退しました。",
            color= 0x40ff40,
        )
        embed.set_thumbnail(url=member.avatar)

        if member.bot == True:
            embed.description = "これはBotアカウントです。"
        else:
            embed.description = f"参加ありがとうございました。"
        
        embed.add_field(
            name="ユーザー名",
            value=member.name
        )

        channel = discord.Client.get_channel(self, 1053378446627188779)
        await channel.send(embed=embed)

        return
