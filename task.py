import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# これから、この app に処理を設定していきます
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    next()


# `/thankyou` というスラッシュコマンドを使うと以下のリスナーが実行されます
@app.command("/mtg")
def handle_command(body, ack, client, logger):
    logger.info(body)
    
    # スラッシュコマンドのリクエストを受け付けたことを Slack に伝えます
    ack()

    # ユーザに対してモーダルを開くメソッドです
    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "gratitude-modal",
            "title": {"type": "plain_text", "text": "感謝を伝えよう 💖", "emoji": True},
            "submit": {"type": "plain_text", "text": "送信"},
            "close": {"type": "plain_text", "text": "キャンセル"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "users-select-block",
                    "element": {
                        "type": "multi_users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "一人または複数人を選択できます",
                        },
                        "action_id": "users-action-id",
                    },
                    "label": {"type": "plain_text", "text": "感謝したい人"},
                },
                {
                    "type": "input",
                    "block_id": "message-block-id",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "message-action-id",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "このメッセージはチャンネルに投稿されるので、他の人にもわかる内容を書いてください",
                        },
                    },
                    "label": {"type": "plain_text", "text": "メッセージ"},
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "「送信」を押したら、#ハッカソン というチャンネルに投稿されます。",
                        }
                    ],
                },
            ],
        },
    )
    logger.info(res)


# ユーザがモーダルからデータ送信したときのリスナーです
@app.view("gratitude-modal")
def view_submission(ack, body, client, logger):
    ack()
    logger.info(body)

    # チャンネル ID を指定することもできます
    push_channel = "#ハッカソン"
    values = body["view"]["state"]["values"]
    users = values["users-select-block"]["users-action-id"]["selected_users"]
    gratitude_message = values["message-block-id"]["message-action-id"]["value"]

    # Slack API 上、他のユーザを直接通知するには、このようにユーザ ID を不等号に入れ、アットマークをつけると綺麗に表示されます <@user_id> 。
    at_users = " ".join([f"<@{name}>" for name in users])

    # チャンネルにメッセージを送信します
    client.chat_postMessage(channel=push_channel, text=f"{at_users} {gratitude_message}")

if __name__ == "__main__":
    # ソケットモードのコネクションを確立
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()