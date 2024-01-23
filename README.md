
# Yone Discord Bot Server Administrator

## Overview

サーバー管理用のDiscordBotです。

## Usage

1. インストール

`requirements.txt` に記述しているモジュールが不足している場合は、以下のコマンドを使用してインストールします。

```
pip install -r requirements.txt
```

2. Configを設定

`src/data/config.py` の `TOKEN`, `LOG_CHANNEL_ID`, `OWNER_USER_ID`, `MAIN_GUILD_ID`, `DATABASE_FILE_PATH`, `REPORT_POST_CHANNEL` に任意の値を指定します。これらが正しく指定されていない場合は動作しません。必要に応じて、その他の定数も指定します。

3. 実行

以下のコマンドを使用してプロジェクトを実行します。

```
python -m YoneDiscordBotServerAdministrator
```

## LICENSE

Licensed under the [Apache License 2.0](https://github.com/yone1130/YoneDiscordBotServerAdministrator/blob/main/LICENSE).

Copyright (c) よね/Yone