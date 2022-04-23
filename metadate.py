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
def handle_shortcuts(ack: Ack, body: dict, context: BoltContext, client: WebClient):
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    ack()

    # モーダルの基礎的なところを組み立てる
    modal_view = {
        "type": "modal",
        "callback_id": "modal-id",
        "title": {"type": "plain_text", "text": "テストモーダル"},
        "submit": {"type": "plain_text", "text": "送信"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "private_metadata": "{}",
        "blocks": [],
    }
    # グローバルショートカットやホームタブのボタンなどだとチャンネルが紐づかないので
    # conversations_select のブロックを置いてそこでチャンネルを指定してもらいます
    if context.channel_id is None:
        modal_view["blocks"].append(
            {
                "type": "input",
                "block_id": "channel_to_notify",
                "element": {
                    "type": "conversations_select",
                    "action_id": "_",
                    # response_urls を発行するためには
                    # このオプションを設定しておく必要があります
                    "response_url_enabled": True,
                    # 現在のチャンネルを初期値に設定するためのオプション
                    "default_to_current_conversation": True,
                },
                "label": { "type": "plain_text", "text": "起動したチャンネル" },
            },
        )
    else:
        # private_metadata に文字列として JSON を渡します
        # スラッシュコマンドやメッセージショートカットは必ずチャンネルがあるのでこれだけで OK
        import json
        state = {"channel_id": context.channel_id}
        modal_view["private_metadata"] = json.dumps(state)

    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        trigger_id=body["trigger_id"],
        view=modal_view,
    )


@app.view("modal-id")
def handle_view_submission(ack: Ack, view: dict, respond: Respond, context: BoltContext):
    ack()
    # 指定されたチャンネルに対して response_url を使ってメッセージを送信します
    respond(text=f"Thanks!<@{context.user_id}>さん!")

# @app.view("modal-id")
# def handle_view_submission(ack: Ack, view: dict, say: Say):
#     ack()
#     # private_metadata か conversations_select ブロックからチャンネル ID を取得
#     import json
#     channel_to_notify = json.loads(view.get("private_metadata", "{}")).get("channel_id")
#     if channel_to_notify is None:
#         channel_to_notify = (
#             view["state"]["values"]
#             .get("channel_to_notify") initial_users
#             .get("_")
#             .get("selected_conversation")
#         )
#     # そのチャンネルに対して chat.postMessage でメッセージを送信します
#     say(channel=channel_to_notify, text="Thanks!")

if __name__ == "__main__":
    # ソケットモードのコネクションを確立
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()