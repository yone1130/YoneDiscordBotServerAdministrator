"""

__main__.py | Yone Discord Bot Server Administrator

Copyright 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import os

import discord
from discord.ext import tasks

from bot.commands import Commands
from bot.events import Events
from data import config
from database import BotDatabase
from errors import *
from voice_channel_check import Voice_channel_check


def main():
    if os.name in ("nt", "dos"):
        os.system("cls")
    else:
        os.system("clear")

    print(
        f"{config.__title__}\n"
        + f"{config.__copyright__}\n\n"
        + f"discord.py  Ver {discord.__version__}\n\n"
        + f"--------------------\n"
    )

    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)
    cmdTree = discord.app_commands.CommandTree(client=client)

    db = BotDatabase(database_file=config.DATABASE_FILE_PATH)

    vc_check = Voice_channel_check()
    voice_check_messages = {}

    Commands(
        client=client,
        cmdTree=cmdTree,
        database=db,
    )

    Events(
        client=client,
        tasks=tasks,
        command_tree=cmdTree,
        database=db,
        vc_check=vc_check,
        voice_check_messages=voice_check_messages,
    )

    client.run(config.TOKEN)  # Login


if __name__ == "__main__":
    main()
