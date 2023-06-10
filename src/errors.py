"""

errors.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord


class UnhandledException:
    def __init__(self, error: Exception) -> str:
        message = f"[ERROR] Unhandled exception. ハンドルされない例外が発生しました。\n{error}"
        print(message)
        return message


class EmbedOfException:
    def __init__(
        self, *, errCode: int, text: str = "", error: Exception
    ) -> discord.Embed:
        return discord.Embed(
            title="Error", description=f"{text}\n```{error}```", color=0xF04040
        ).set_footer(text=f"Error Code: 0x{hex(errCode)}")


class EmbedOfUnhandledException:
    def __init__(self, *, error: Exception) -> discord.Embed:
        return EmbedOfException(errCode=0x0101, text="ハンドルされない例外が発生しました。", error=error)
