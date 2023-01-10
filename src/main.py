#
# main.py | Yone Discord Bot Server Administrator
#
# (c) 2022-2023 よね/Yone
#

import os

import discord
from discord.ext import commands

from YoneDiscordBotServerAdministrator import discordBot
from data import config

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

bot = discordBot(command_prefix = '!', intents=intents)

bot.run(config.TOKEN)  # Login