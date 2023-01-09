#
# main.py | Yone Discord Bot Server Administrator
#
# (c) 2022-2023 よね/Yone
#

import os

import discord
from discord.ext import commands

from data import config

# -------------------- Init -------------------- #
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

print(
    f"Yone Discord Bot Server Administrator\n"+\
    f"(c) 2022-2023 よね/Yone\n\n"+\
    f"discord.py  Ver {discord.__version__}\n\n"+\
    f"--------------------\n"
)


# ---------- Instance ---------- #
class Cmd(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()
        return

#discord
intents = discord.Intents.all()
intents.message_content = True
bot = Cmd(command_prefix = '!', intents=intents)


# -------------------- Events -------------------- #
# ---------- On ready ---------- #
@bot.event
async def on_ready():
    print(">Ready.  Waiting for any command and message\n")


# ----- messages ----- #
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.author.guild_permissions.administrator:
        pass

    else:
        if len(message.mentions) >= 2:
            await message.reply(
                embed=discord.Embed(
                    title="警告",
                    description="__**大量メンション行為は禁止です。**__\n"+
                                "__該当メッセージは削除されます。__\n"+
                                "※この警告メッセージは１０秒後に自動削除します。",
                    color=0xff4040
                )
                .set_footer(
                    text="警告種別コード: 0x01001"
                ),
                delete_after=10
            )
            await message.delete()

    return


# ----- Member join ----- #
@bot.event
async def on_member_join(member):

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

    channel = bot.get_channel(1053378446627188779)
    await channel.send(embed=embed)

    return


# ----- Member remove ----- #
@bot.event
async def on_member_remove(member):

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

    channel = bot.get_channel(1053378446627188779)
    await channel.send(embed=embed)

    return


# -------------------------------------------------- #
# -------------------- Commands -------------------- #
# -------------------------------------------------- #
@bot.hybrid_command(name="ping")
async def ping(ctx):
    await ctx.reply("Pong!")


# ---------- RUN ---------- #
bot.run(config.TOKEN)  # Login
