"""

errors.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0

"""

import discord


def UnhandledException(error: Exception) -> None:
    """ハンドルされない例外をprint"""
    message = f"[ERROR] Unhandled exception. ハンドルされない例外が発生しました。\n{error}"
    print(message)


def EmbedOfException(*, err_code: int, text: str = "", error: Exception) -> discord.Embed:
    """例外表示用のembedを生成

    Args:
        err_code (int): エラーコード。16進数として取り扱う。0x形式で記述
        text (str): 表示する説明文
        error (Exception)

    Returns:
        discord.Embed: 生成したembed
    """
    return discord.Embed(
        title="Error",
        description=f"{text}\n```{error}```",
        color=0xF04040
    ).set_footer(text=f"Error Code: {hex(err_code)}")


def EmbedOfUnhandledException(*, error: Exception) -> discord.Embed:
    """ハンドルされない例外表示用のembedを生成"""
    return EmbedOfException(errCode=0x0101, text="ハンドルされない例外が発生しました。", error=error)
