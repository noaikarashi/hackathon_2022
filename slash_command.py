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
def handle_some_command(ack: Ack, body: dict, client: WebClient):
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    ack()
    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        # 上記で説明した trigger_id で、これは必須項目です
        # この値は、一度のみ 3 秒以内に使うという制約があることに注意してください
        trigger_id=body["trigger_id"],
        # モーダルの内容を view オブジェクトで指定します
        view={
            # このタイプは常に "modal"
            "type": "modal",
            # このモーダルに自分で付けられる ID で、次に説明する @app.view リスナーはこの文字列を指定します
            "callback_id": "modal-id",
            # これは省略できないため、必ず適切なテキストを指定してください
            "title": {"type": "plain_text", "text": "テストモーダル"},
            # input ブロックを含まないモーダルの場合は view から削除することをおすすめします
            # このコード例のように input ブロックがあるときは省略できません
            "submit": {"type": "plain_text", "text": "送信"},
            # 閉じるボタンのラベルを調整することができます（必須ではありません）
            "close": {"type": "plain_text", "text": "閉じる"},
            # Block Kit の仕様に準拠したブロックを配列で指定
            # 見た目の調整は https://app.slack.com/block-kit-builder を使うと便利です
            "blocks": [
                {
                    # 様々なブロックのうち input ブロックだけがデータ送信に含まれます
                    # ブロックの一覧はこちら: https://api.slack.com/reference/block-kit/blocks
                    "type": "input",
                    # block_id / action_id を指定しない場合 Slack がランダムに指定します
                    # この例のように明に指定することで、@app.view リスナー側での入力内容の取得で
                    # ブロックの順序に依存しないようにすることをおすすめします
                    "block_id": "question-block",
                    # ブロックエレメントの一覧は https://api.slack.com/reference/block-kit/block-elements
                    # Works with block types で Input がないものは input ブロックに含めることはできません
                    "element": {"type": "plain_text_input", "action_id": "input-element"},
                    # これはモーダル上での見た目を調整するものです
                    # 同様に placeholder を指定することも可能です 
                    "label": {"type": "plain_text", "text": "質問"}
                }
            ],
        },
    )

    # ユーザがモーダルからデータ送信したときのリスナーです
@app.view("modal-id")
def view_submission(ack: Ack, body: dict, client: WebClient, logger):
    ack()
    logger.info(body)

    # チャンネル ID を指定することもできます
    thank_you_channel = "#ハッカソン"
    values = body["view"]["state"]["values"]
    users = values["question-block"]["input-element"]
    # gratitude_message = values["message-block-id"]["message-action-id"]["value"]

    # Slack API 上、他のユーザを直接通知するには、このようにユーザ ID を不等号に入れ、アットマークをつけると綺麗に表示されます <@user_id> 。
    # at_users = " ".join([f"<@{name}>" for name in users])

    # チャンネルにメッセージを送信します
    client.chat_postMessage(channel=thank_you_channel, text=f"{users}")  #{gratitude_message}


# アプリを起動します
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()