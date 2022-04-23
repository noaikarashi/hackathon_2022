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
def handle_some_command(ack: Ack, body: dict, client: WebClient, context: BoltContext):
        ack()        
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                # このタイプは常に "modal"
                "type": "modal",
                # このモーダルに自分で付けられる ID で、次に説明する @app.view リスナーはこの文字列を指定します
                "callback_id": "modal-id",

                "title": { "type": "plain_text", "text": "ミーティングの設定 :pencil:", "emoji": True },
                "submit": { "type": "plain_text", "text": "送信", "emoji": True },
                "type": "modal",
                "close": { "type": "plain_text", "text": "キャンセル", "emoji": True },
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "input-title",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "title",
                            "placeholder": { "type": "plain_text", "text": "ミーティングのタイトルを入力してください", "emoji": True }
                        },
                        "label": { "type": "plain_text", "text": "件名", "emoji": True},
                        "optional": False
                    },
                    {
                        "type": "input",
                        "block_id": "input-assignee",
                        "element": {
                            "type": "multi_users_select",
                            "action_id": "multi_users_select",
                            "placeholder": { "type": "plain_text", "text": "ミーティングに参加するユーザを選択してください", "emoji": True}
                        },
                        "label": { "type": "plain_text", "text": "参加者", "emoji": True},
                        "optional": True
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "static_select",
                            "action_id": "place",
                            "placeholder": { "type": "plain_text", "text": "活動場所を選択してください", "emoji": True },
                        "options": [
                            {
                                "text": { "type": "plain_text", "text": "Zoom", "emoji": True },
                                "value": "value-0"
                            },
                            {
                                "text": { "type": "plain_text", "text": "Discord", "emoji": True },
                                "value": "value-1"
                            },
                            {
                                "text": { "type": "plain_text", "text": "Gather", "emoji": True },
                                "value": "value-2"
                            },
                            {
                                "text": { "type": "plain_text", "text": "その他", "emoji": True },
                                "value": "value-3"
                            }
                        ]
                        },
                        "label": { "type": "plain_text", "text": "活動場所", "emoji": True }
                    },
                    {
                        "type": "input",
                        "block_id": "input-deadline",
                        "element": {
                            "type": "datepicker",
                            "action_id": "day",
                            "placeholder": { "type": "plain_text", "text": "日付を選択してください", "emoji": True }
                        },
                        "label": { "type": "plain_text", "text": "開催日", "emoji": True },
                        "optional": True
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "timepicker",
                            "action_id": "timepicker-action",
                            "initial_time": "12:00",
                            "placeholder": { "type": "plain_text", "text": "Select time", "emoji": True },
                        },
                        "label": { "type": "plain_text", "text": "開始時刻", "emoji": True }
                    },
                    {
                        "type": "input",
                        "block_id": "input-description",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "detail",
                            "multiline": True,
                            "placeholder": { "type": "plain_text", "text": "できるだけ具体的に記入してください", "emoji": True }
                        },
                        "label": { "type": "plain_text", "text": "詳細内容", "emoji": True },
                        "optional": True
                    }
                ]
            }
        )


# モーダルsubmit受信側
@app.view("modal-id")
def handle_view_events(ack: Ack, view: dict, logger: logging.Logger):
    # 送信された input ブロックの情報はこの階層以下に入っています
    inputs = view["state"]["values"]
    # 最後の "value" でアクセスしているところはブロックエレメントのタイプによっては異なります
    # パターンによってどのように異なるかは後ほど詳細を説明します
    question = inputs.get("question-block", {}).get("input-element", {}).get("value")
    # 入力チェック
    if len(question) < 5:
        # エラーメッセージをモーダルに表示
        # （このエラーバインディングは input ブロックにしかできないことに注意）
        ack(response_action="errors", errors={"question-block": "質問は 5 文字以上で入力してください"})
        return

    # 正常パターン、実際のアプリではこのタイミングでデータを保存したりする
    logger.info(f"Received question: {question}")

    # 空の応答はこのモーダルを閉じる（ここまで 3 秒以内である必要あり）
    ack()

# アプリを起動します
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()