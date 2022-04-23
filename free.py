import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# ボットトークンと署名シークレットを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/mtg")
def test_response_url(ack: Ack):
    ack(
        text="ボタンやセレクトメニューのテストです",
        blocks=[
            {
                "type": "actions",
                "elements": [
                    # これらのボタン・セレクトメニューを操作すると
                    # block_actions というイベントが発生します
                    # この場合は必ず response_url が発行されます
                    {
                        "type": "button",
                        "action_id": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "クリック！",
                        },
                        "value": "start",
                    },
                    {
                        "type": "users_select",
                        "action_id": "users-select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "ユーザーを選ぶ",
                        },
                    },
                ]
            }
        ],
    )

@app.action("button")
def start(ack: Ack, body: dict, action: dict, respond: Respond, context: BoltContext):
    assert body.get("response_url") is not None
    ack()
    # メッセージ内のボタンから来たので常に response_url が存在します
    respond(f"受け取った内容: {action}", replace_original=False)
    respond(f"<@{context.user_id}>さん！")

@app.action("users-select")
def start(ack: Ack, body: dict, action: dict, respond: Respond):
    assert body.get("response_url") is not None
    ack()
    # メッセージ内のセレクトメニューから来たので常に response_url が存在します
    respond(f"受け取った内容: {action}", replace_original=False)



# アプリを起動します
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()