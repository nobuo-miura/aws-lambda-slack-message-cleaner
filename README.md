# AWS Lambda - Slack Message Cleaner

指定時間前のSlackのメッセージを削除します。

本スクリプトはLambda向けに作成しています。



This script deletes Slack messages prior to a specified time.

The script is designed for use with Lambda.



## ○Lambda

- [Python 3.9](https://github.com/yinyangdev/docker-aws)

  ```shell
  git clone https://github.com/yinyangdev/aws-lambda-slack-message-cleaner.git
  cd aws-lambda-slack-message-cleaner
  pip install slack_sdk -t .
  chmod -R 755 ./*
  zip -r lambda.zip *
  ```

  

## ○ Event

```json
{
  "Token": "xoxp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "Term": 0,
  "Sleep": 1,
  "BotOnly": "True",
  "Channels": [
    "xxxxxxxxx",
    "xxxxxxxxx"
  ]
}
```

- Token - Slack App Token (channels:history / groups:history / im:history / mpim:history /chat:write)
- Term - Delete messages older second (s)
- Sleep - Message Delete Interval (s)
- BotOnly - If True, remove only the BOT
- Channels - Slack Channel ID



