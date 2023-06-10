"""

__main__.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import os
import sqlite3

import discord
from discord.ext import tasks

try:
    from bot.commands import Commands
    from bot.events import Events
    from data import config
    from errors import *
    from voice_channel_check import *

except ModuleNotFoundError as error:
    print(f"[ERROR] {error}")


clearConsole = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")
clearConsole()

print(
    f"Yone Discord Bot Server Administrator\n"
    + f"(c) 2022-2023 よね/Yone\n\n"
    + f"discord.py  Ver {discord.__version__}\n\n"
    + f"--------------------\n"
)


intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
cmdTree = discord.app_commands.CommandTree(client=client)


db_con = sqlite3.connect("bot-savedata.db")
db_cur = db_con.cursor()

db_cur.execute("CREATE TABLE IF NOT EXISTS globalBannedList(uid, datetime)")
db_cur.execute("CREATE TABLE IF NOT EXISTS vcAlertDisableChannels(channelId)")
db_con.commit()


vc_check = Voice_channel_check()
voice_check_messages = {}

Commands(
    client=client,
    tasks=tasks,
    cmdTree=cmdTree,
    vc_check=vc_check,
    db_con=db_con,
    db_cur=db_cur,
)

Events(client=client, tasks=tasks, command_tree=cmdTree, db_cur=db_cur, vc_check=vc_check)


client.run(config.TOKEN)  # Login
