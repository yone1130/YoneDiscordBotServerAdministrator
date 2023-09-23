"""

__main__.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone

Licensed under the Apache License 2.0

"""

import os
import discord
from discord.ext import tasks


class YoneDiscordBotServerAdministrator:
    CONFIG_FILE_PATH = "data/config.py"

    def __init__(self) -> None:
        try:
            self.clear_console()
            self.import_modules()

            print(
                f"{self.config.__title__}\n"
                f"{self.config.__copyright__}\n\n"
                f"discord.py  Ver {discord.__version__}\n\n"
                f"--------------------\n"
            )

            try:
                intents = discord.Intents.all()
                intents.message_content = True
                client = discord.Client(intents=intents)
                cmdTree = discord.app_commands.CommandTree(client=client)
            except Exception as error:
                self.error(
                    error_code=0x0203,
                    text="Discord client initialisation has failed.",
                    error=error,
                )
                raise error

            try:
                self.errors = self.Errors(client=client)
                db = self.BotDatabase(
                    database_file=self.config.DISCORD_BOT_DATA["databaseFilePath"]
                )
                vc_check = self.Voice_channel_check()
                voice_check_messages = {}
            except Exception as error:
                self.error(
                    error_code=0x0204,
                    text="Discord client initialisation has failed.",
                    error=error,
                )
                raise error

            try:
                self.Commands(
                    client=client,
                    errors=self.errors,
                    cmdTree=cmdTree,
                    database=db,
                )
            except Exception as error:
                self.error(
                    error_code=0x0205,
                    text="Discord commands object initialisation has failed.",
                    error=error,
                )

            try:
                self.Events(
                    client=client,
                    errors=self.errors,
                    tasks=tasks,
                    command_tree=cmdTree,
                    database=db,
                    vc_check=vc_check,
                    voice_check_messages=voice_check_messages,
                )
            except Exception as error:
                self.error(
                    error_code=0x0206,
                    text="Discord events object initialisation has failed.",
                    error=error,
                )

            client.run(token=self.config.DISCORD_BOT_DATA["token"])  # Login

            return

        except Exception as error:
            self.error(
                error_code=0x0202, text="Unhandled exception has occurred.", error=error
            )

    def clear_console(self) -> int:
        if os.name in ("nt", "dos"):
            return os.system(command="cls")
        else:
            return os.system(command="clear")

    def import_modules(self) -> None:
        if os.path.exists(self.CONFIG_FILE_PATH):
            from data import config

            self.config = config
        else:
            self.error_file_not_found(self.CONFIG_FILE_PATH)

        for file in config.APPLICATION_FILES:
            if os.path.exists(file) is False:
                self.error_file_not_found(file_path=file)

        from bot.commands import Commands
        from bot.events import Events
        from database import BotDatabase
        from errors import Errors
        from voice_channel_check import Voice_channel_check

        self.Errors = Errors
        self.Commands = Commands
        self.Events = Events
        self.BotDatabase = BotDatabase
        self.Voice_channel_check = Voice_channel_check

        return

    def error_file_not_found(self, file_path):
        print(
            f"\n"
            f"[ERROR]\n"
            f"File not found.\n"
            f"The {file_path} required for this bot start-up has not been found."
            f"Error code: {hex(0x0201)}\n",
            end="\n\n",
        )
        exit()

    def error(self, *, error_code: int, text: str, error: Exception) -> None:
        print(
            f"[ERROR]\n"
            f"Error code: {hex(error_code)}\n"
            f"{text}\n"
            f"Exception: {error}",
            end="\n\n",
        )
        raise error


if __name__ == "__main__":
    YoneDiscordBotServerAdministrator()
