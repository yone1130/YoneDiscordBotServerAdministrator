
# Yone Discord Bot Server Administrator

## About

サーバー管理用のDiscordBotです。

## Usage Technology

#### Langages / Libraries

- Python
- discord.py

## How to Use

1. 必要なモジュールをインストール。

[./requirements.txt](https://github.com/yone1130/YoneDiscordBotServerAdministrator/blob/main/requirements.txt) に記述しているモジュールが不足している場合は、以下のコマンドを使用してインストール。

```
$ pip install -r requirements.txt
```

2. Configを設定

[./src/data/config.py](https://github.com/yone1130/YoneDiscordBotServerAdministrator/blob/main/src/data/config.py) の `TOKEN`, `LOG_CHANNEL_ID`, `OWNER_USER_ID`, `MAIN_GUILD_ID`, `DATABASE_FILE_PATH`, `REPORT_POST_CHANNEL` に任意の値を指定してください。これらが正しく指定されていない場合は動作しません。必要に応じて、その他の定数も指定してください。

3. プロジェクトを実行

```
$ python -m YoneDiscordBotServerAdministrator
```

## LICENSE
Apache License 2.0
[License File](https://github.com/yone1130/YoneDiscordBotServerAdministrator/blob/main/LICENSE)
