"""

__main__.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import os
import discord
from data import config
import datetime
import sqlite3


# -------------------- Init -------------------- #
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

print(
    f"Yone Discord Bot Server Administrator\n"+\
    f"(c) 2022-2023 よね/Yone\n\n"+\
    f"discord.py  Ver {discord.__version__}\n\n"+\
    f"--------------------\n"
)

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
cmdTree = discord.app_commands.CommandTree(client=client)

db_con = sqlite3.connect("bot-savedata.db")
db_cur = db_con.cursor()

db_cur.execute("CREATE TABLE IF NOT EXISTS globalBannedList(uid, datetime)")
db_con.commit()


# -------------------- Main -------------------- #
#  ---------- Events ---------- #
# ----- On ready ----- #
@client.event
async def on_ready():
    await cmdTree.sync()
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
                    title="Pong",
                    description="Hi",
                    color=0x40ff40
                )
            )
            return

        if len(message.mentions) >= 5:
            await message.reply(
                embed=discord.Embed(
                    title="⚠警告⚠",
                    description="大量メンション行為は禁止です。\n"+
                                "該当メッセージは削除されます。\n"+
                                "※この警告メッセージは１５秒後に自動削除します。",
                    color=0xff4040
                )
                .set_footer(
                    text="警告種別コード: 0x0101"
                ),
                delete_after=15
            )
            await message.delete()

            channel = client.get_channel(config.spamChannels[message.guild.id])
            await channel.send(
                embed=discord.Embed(
                    title="スパム行為を検出",
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


# ----- On member join ----- #
@client.event
async def on_member_join(member):
    # log
    if member.guild.id in config.joinedChannels:
        embed=discord.Embed(
            title=f"{member.name} が参加しました。",
            color= 0x40ff40,
        )
        embed.set_thumbnail(url=member.avatar)

        if member.bot:
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
            value=member.mention
        )
        embed.add_field(
            name="アカウントの作成日時",
            value=created_at
        )
        channel = client.get_channel(config.joinedChannels[member.guild.id])
        await channel.send(embed=embed)

    # global ban
    try:
        db_cur.execute(f"SELECT uid FROM globalBannedList WHERE uid=?", (str(member.id),))
        data = db_cur.fetchall()

    except Exception as e:
        print(f"[ERROR] {e}")
        return

    if data:
        try:
            await member.ban(reason="グローバルBANリストに登録されているため")

            try:
                embed=discord.Embed(
                    title="Global Ban",
                    description=f"{member.name} はグローバルBANリストに登録されているため、BANされました。",
                    color= 0x40ff40,
                )
                embed.set_thumbnail(url=member.avatar)
                channel = client.get_channel(config.joinedChannels[member.guild.id])
                await channel.send(embed=embed)

            except:
                pass

        except Exception as e:
            try:
                embed=discord.Embed(
                    title=f"エラーが発生しました",
                    color= 0xff4040,
                    description=f"{member.name} はグローバルBANリストに登録されているため、BANを試みましたが失敗しました。```{e}```"
                )
                embed.set_thumbnail(url=member.avatar)
                embed.set_footer(
                    text=f"エラーコード: 0x0301"
                )

                channel = client.get_channel(config.joinedChannels[member.guild.id])
                await channel.send(embed=embed)

            except:
                pass


    # welcome
    if member.bot == False:
        if member.guild.id in config.welcomeChannels:
            channel = client.get_channel(config.welcomeChannels[member.guild.id])
            ruleChannel = client.get_channel(config.ruleChannels[member.guild.id])

            if member.guild.id in {1053378444781703339}:  # My server
                await channel.send(
                    content=f"{member.mention} さん。\n\n"+
                            f"ようこそ {member.guild.name} へ！\n"+
                            f"Welcome to {member.guild.name}!\n\n"+
                             "参加いただきありがとうございます。\n"+
                             "Thank you for joining.\n\n"+
                             "必ずガイドラインをご確認ください。\n"+
                             "Please check the guidelines.\n"+
                            f"{ruleChannel.mention}\n\n"
                )

            else:  # Other guild
                await channel.send(
                    content=f"{member.mention} さん。\n\n"+
                            f"ようこそ {member.guild.name} へ！\nWelcome to {member.guild.name}!\n\n"+
                                "必ずルールをご確認ください。\nPlease check the rule.\n"+
                            f"{ruleChannel.mention}"
                )

    return


# ----- On member remove ----- #
@client.event
async def on_member_remove(member):
    if  member.guild.id in config.joinedChannels:
        embed=discord.Embed(
            title=f"{member.name} が脱退しました。",
            color= 0x40ff40,
        )
        embed.set_thumbnail(url=member.avatar)

        if member.bot == True:
            embed.description = "これはBotアカウントです。"

        else:
            embed.description = f"参加ありがとうございました。"

        embed.add_field(
            name="ユーザー名",
            value=member.mention
        )
        channel = client.get_channel(config.joinedChannels[member.guild.id])
        await channel.send(embed=embed)

    return

# ----- On reaction add ----- #
@client.event
async def on_raw_reaction_add(reaction):
    if  reaction.message_id in []:
        roles = reaction.member.guild.get_role(config.memberRoles[reaction.member.guild.id])
        await reaction.member.add_roles(roles, reason="ガイドラインに同意しました。")

    return


# ---------- Commands ---------- #
@discord.app_commands.guilds(discord.Object(id=0))

# ----- info ----- #
@cmdTree.command(
    name="info",
    description="Send bot information"
)
async def info(inter: discord.Interaction):
    embed = discord.Embed(
        title="Yone Bot Server Administrator",
        color= 0x40ff40,
        description='(c) 2022-2023 よね/Yone\n'+
                    '不具合等の連絡は <@892376684093898772> までお願いいたします。'
    )
    await inter.response.send_message(embed=embed)
    return


# ----- clear ----- #
@cmdTree.command(
    name="clear",
    description="Clear message(s)"
)
async def clear(inter: discord.Interaction, target:int):
    if inter.user.guild_permissions.administrator:
        await inter.response.send_message(content="Please while...")

        deleted = await inter.channel.purge(
            limit=target+1,
            reason=f"{inter.user.name} が /clear を使用しました。"
        )

        embed = discord.Embed(
            title="Deleted messages",
            color= 0x40ff40,
            description=f"{len(deleted)-1}個のメッセージを削除しました。\n"+
                        f"{inter.user.mention} が /clear を使用しました。"
        )

        await inter.channel.send(embed=embed, delete_after=10)

        return
    
    else:
        embed = discord.Embed(
            title="Error",
            color= 0xff4040,
            description="あなたはこのコマンドを実行する権限がありません。"
        )
        await inter.response.send_message(embed=embed, ephemeral=True)
        return


# ----- global ban add ----- #
@cmdTree.command(
    name="gban-add",
    description="User add to global banned list."
)
async def gban_add(inter: discord.Interaction, target: discord.Member):
    if inter.user.guild_permissions.administrator:
        try:
            db_cur.execute(f"SELECT uid, datetime FROM globalBannedList WHERE uid=?", (str(target.id),))
            data = db_cur.fetchall()

        except Exception as e:
            await inter.response.send_message(
                embed=discord.Embed(
                    title="エラーが発生しました",
                    color= 0xff4040,
                    description=f"データベースの読み込みに失敗しました。```{e}```"
                )
                .set_footer(
                    text=f"エラーコード: 0x0201"
                ),
                ephemeral=True
            )
            return

        if (not data) or (data is None):
            dt_Now = datetime.datetime.now()
            add_datetime = dt_Now.strftime('%Y%m%d%H%M%S')

            insertData = (str(target.id), add_datetime)
            db_cur.execute("INSERT INTO globalBannedList VALUES(?, ?)", insertData)
            db_con.commit()

            await inter.response.send_message(
                embed=discord.Embed(
                    title="Global Ban",
                    color= 0x40ff40,
                    description= f"{target.mention} をGlobal Bannedリストに登録しました。"
                ),
                ephemeral=True
            )
            return
        
        else:
            await inter.response.send_message(
                embed=discord.Embed(
                    title="Global Ban",
                    color= 0xff4040,
                    description= "このユーザーはすでにGlobal Bannedリストに登録されています。"
                ),
                ephemeral=True
            )
            return

    else:
        embed = discord.Embed(
            title="Error",
            color= 0xff4040,
            description="あなたはこのコマンドを実行する権限がありません。"
        )
        await inter.response.send_message(embed=embed, ephemeral=True)
        return


# ----- global ban remove ----- #
@cmdTree.command(
    name="gban-rmv",
    description="User remove from global banned list."
)
@discord.app_commands.describe(
    target="リストから削除するユーザーのID"
)
async def gban_rmv(inter: discord.Interaction, target:str):
    if inter.user.guild_permissions.administrator:
        try:
            db_cur.execute(f"SELECT uid FROM globalBannedList WHERE uid=?", (target,))
            data = db_cur.fetchall()

        except Exception as e:
            await inter.response.send_message(
                embed=discord.Embed(
                    title="エラーが発生しました",
                    color= 0xff4040,
                    description=f"データベースの読み込みに失敗しました。```{e}```"
                )
                .set_footer(
                    text=f"エラーコード: 0x0201"
                ),
                ephemeral=True
            )
            return

        if data:
            db_cur.execute("DELETE FROM globalBannedList WHERE uid=?", (target,))
            db_con.commit()

            await inter.response.send_message(
                embed=discord.Embed(
                    title="Global Ban",
                    color= 0x40ff40,
                    description= f"<@{target}> をGlobal Bannedリストから削除しました。"
                ),
                ephemeral=True
            )
            return
        
        else:
            await inter.response.send_message(
                embed=discord.Embed(
                    title="Global Ban",
                    color= 0xff4040,
                    description= "このユーザーIDはGlobal Bannedリストに登録されていません。"
                ),
                ephemeral=True
            )
            return

    else:
        embed = discord.Embed(
            title="Error",
            color= 0xff4040,
            description="あなたはこのコマンドを実行する権限がありません。"
        )
        await inter.response.send_message(embed=embed, ephemeral=True)
        return


# ---------- Run ---------- #
client.run(config.TOKEN)  # Login

