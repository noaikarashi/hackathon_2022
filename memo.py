import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# これから、この app に処理を設定していきます
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.shortcut("open_modal") 
def handle_shortcuts(ack: Ack, body: dict, client: WebClient):
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    ack()
    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "テストモーダル"},
            "submit": {"type": "plain_text", "text": "送信"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [
                {
                    "type": "section",
                    # block_id はモーダル内でユニークでなければならない
                    "block_id": "user-section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "これは section ブロックです",
                    },
                    "accessory": {
                        "type": "users_select",
                        # action_id がこのモーダル内でユニークである必要はない
                        "action_id": "section-block-users-select",
                    },
                },
                {
                    "type": "input",
                    "block_id": "text-input",
                    "element": {"type": "plain_text_input", "action_id": "action-id"},
                    "label": {"type": "plain_text", "text": "テキスト"},
                },
                {
                    "type": "input",
                    "block_id": "date-input",
                    "element": {"type": "datepicker", "action_id": "action-id"},
                    "label": {"type": "plain_text", "text": "日付"},
                },
            ],
        },
    )

# sections ブロックの選択がされたときに呼び出されます
@app.action("section-block-users-select")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)

# 「送信」ボタンが押されたときに呼び出されます
@app.view("modal-id")
# @app.view({"type": "view_closed", "callback_id": "modal-id"})
def handle_view_submission(ack: Ack, view: dict, logger: logging.Logger):
    ack()
    # state.values.{block_id}.{action_id}
    logger.info(view["state"]["values"])

if __name__ == "__main__":
    # ソケットモードのコネクションを確立
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()