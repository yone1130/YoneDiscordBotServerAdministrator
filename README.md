# Yone Discord Bot Server Administrator

[→ 日本語](./README_JP.md)

## Overview

Discord server administration bot

## Usage

1. Install

```
pip install -r requirements.txt
```

2. Setup Config

Specify any value in `token`, `logChannelId`, `ownerUserId`, `mainGuildId`, `databaseFilePath`, `reportPostChannelId` in `src/data/config.py`. If these are not specified correctly, the operation will not work.  
Specify other constants as needed.

3. Run

```
python -m src
```

## LICENSE

Licensed under the [Apache License 2.0](./LICENSE).

Copyright (C) よね/Yone
