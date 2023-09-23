"""

database.py | Yone Discord Bot Server Administrator

(c) 2022-2023 よね/Yone

Licensed under the Apache License 2.0

"""

import sqlite3
import discord


class BotDatabase:
    """データベース操作クラス"""

    def __init__(self, *, database_file: str) -> None:
        """
        Args:
            database_file (str): 使用するデータベースのファイルパス名
        """
        self.database_file = database_file
        self.create_table()

    def connect(self) -> sqlite3.Connection:
        """データベース接続"""
        return sqlite3.connect(self.database_file)

    def cursor(self, *, connect: sqlite3.Connection) -> sqlite3.Cursor:
        """データベースカーソルインスタンスを生成"""
        return connect.cursor()

    def save(self, *, connect: sqlite3.Connection) -> None:
        """データベース保存

        データベース操作内容のコミットおよびクローズを行う
        """
        connect.commit()
        connect.close()

    def create_table(self) -> None:
        """データベースのテーブル作成"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute("CREATE TABLE IF NOT EXISTS globalBannedList(uid, datetime)")
        db_cur.execute("CREATE TABLE IF NOT EXISTS vcAlertDisableChannels(channelId)")
        self.save(connect=db_con)

    def get_gban(self, *, target: discord.User.id) -> list:
        """グローバルBANリストの取得"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute(
            f"SELECT uid, datetime FROM globalBannedList WHERE uid=?", (str(target),)
        )
        data = db_cur.fetchall()
        self.save(connect=db_con)
        return data

    def insert_gban(self, *, target: discord.User.id, add_datetime: str) -> None:
        """グローバルBANリストへ追加"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute(
            "INSERT INTO globalBannedList VALUES(?, ?)", (str(target), add_datetime)
        )
        self.save(connect=db_con)

    def delete_gban_user(self, *, target: discord.User.id) -> None:
        """グローバルBANリストから削除"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute("DELETE FROM globalBannedList WHERE uid=?", (target,))
        self.save(connect=db_con)

    def get_vc_alert_disable_channels(self, *, target: discord.User.id) -> list:
        """VC Long Time Alert 機能を無効にするチャンネルリストを取得"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute(
            f"SELECT channelId FROM vcAlertDisableChannels WHERE channelId=?",
            (str(target),),
        )
        data = db_cur.fetchall()
        self.save(connect=db_con)
        return data

    def insert_vc_alert_disable_channels(self, *, target: discord.User.id) -> None:
        """VC Long Time Alert 機能を無効にするチャンネルリストへ追加"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute("INSERT INTO vcAlertDisableChannels VALUES(?)", (str(target),))
        self.save(connect=db_con)

    def delete_vc_alert_disable_channels(self, *, target: discord.User.id) -> None:
        """VC Long Time Alert 機能を無効にするチャンネルリストから削除"""
        db_con = self.connect()
        db_cur = self.cursor(connect=db_con)
        db_cur.execute(
            "DELETE FROM vcAlertDisableChannels WHERE channelId=?", (str(target),)
        )
        self.save(connect=db_con)
