import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# これから、この app に処理を設定していきます
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("hello")
def message_hello(message, say):
    {
        "blocks": [
            {
                "type": "header",
                "text": { "type": "plain_text", "text": ":newspaper:  MTG通知  :newspaper:"}
            },
            {
                "type": "context",
                "elements": [
                    { "text": "開催日*November 12, 2019*  |  ", "type": "mrkdwn"}
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": { "type": "mrkdwn", "text": " :loud_sound: *件名* :loud_sound:" }
            },
            {
                "type": "section",
                "text": { "type": "mrkdwn", "text": "Replay our screening of *Threat Level Midnight* ." },
                "accessory": {
                    "type": "button",
                    "text": { "type": "plain_text", "text": "Watch Now", }
                }
            },
            {
                "type": "section",
                "text": { "type": "mrkdwn", "text": "The *2019 Dundies* happened. \nAwards " }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": { "type": "mrkdwn", "text": ":calendar: |   *日時*  | :calendar: " }
            },
            {
                "type": "section",
                "text": { "type": "mrkdwn", "text": "`11/20-11/22` *Beet th* _ annual retreat at Schrute Farms_" },
                "accessory": {
                    "type": "button",
                    "text": { "type": "plain_text", "text": "RSVP", }
                }
            },
            {
                "type": "section",
                "text": { "type": "mrkdwn", "text": "`12/01` *Toby's Going Away Party* at _Benihana_" },
                "accessory": {
                    "type": "button",
                    "text": { "type": "plain_text", "text": "Learn More", }
                }
            },
            {
                "type": "section",
                "text": { "type": "mrkdwn", "text": "`11/13` :pretzel: *Pretzel Day* :pretzel: at _Scranton Office_" },
                "accessory": {
                    "type": "button",
                    "text": { "type": "plain_text", "text": "RSVP", "emoji": true
                    }
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":calendar: |   *場所*  | :calendar: "
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "`10/21` *Conference Room Meeting*"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Watch Recording",
                        "emoji": true
                    }
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*詳細内容*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":printer: *Sabre Printers*",
                    "verbatim": false
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Please join me in welcoming our 3 "
                }
            },
            {
                "type": "divider"
            }
        ]
    }

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()