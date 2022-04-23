import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# ボットトークンと署名シークレットを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    next()

@app.command("/mtg")
def handle_some_command(body, ack, client, logger):
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    logger.info(body)
    ack()
    # views.open という API を呼び出すことでモーダルを開きます
    res = client.views_open(
        # 上記で説明した trigger_id で、これは必須項目です
        # この値は、一度のみ 3 秒以内に使うという制約があることに注意してください
        trigger_id=body["trigger_id"],
        # モーダルの内容を view オブジェクトで指定します
        view={
            # このタイプは常に "modal"
            "type": "modal",
            # このモーダルに自分で付けられる ID で、次に説明する @app.view リスナーはこの文字列を指定します
            "callback_id": "modal-id",

            "title": { "type": "plain_text", "text": "ミーティングの設定 :pencil:" },
            "submit": { "type": "plain_text", "text": "送信" },
            "type": "modal",
            "close": { "type": "plain_text", "text": "キャンセル" },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title-block-id",
                    "element": {
                        "type": "plain_text_input",
                        "placeholder": { "type": "plain_text", "text": "ミーティングのタイトルを入力してください" },
                        "action_id": "title-action-id",
                    },
                    "label": { "type": "plain_text", "text": "件名" },
                },
                {
                    "type": "input",
                    "block_id": "users-block-id",
                    "element": {
                        "type": "multi_users_select",
                        "placeholder": { "type": "plain_text", "text": "ミーティングに参加するユーザを選択してください" },
                        "action_id": "users-action-id",
                    },
                    "label": { "type": "plain_text", "text": "参加者" }
                },
                {
		        	"type": "input",
                    "block_id": "place-block-id",
			        "element": {
                        "type": "static_select",
                        "placeholder": { "type": "plain_text", "text": "活動場所を選択してください" },
                        "action_id": "place-action-id",
				    "options": [
					    {
                            "text": { "type": "plain_text", "text": "Zoom" },
                            "value": "value-0"
                        },
                        {
                            "text": { "type": "plain_text", "text": "Discord" },
                            "value": "value-1"
                        },
                        {
                            "text": { "type": "plain_text", "text": "Gather" },
                            "value": "value-2"
                        },
                        {
                            "text": { "type": "plain_text", "text": "その他" },
                            "value": "value-3"
                        }
	    			]
			        },
			        "label": { "type": "plain_text", "text": "活動場所" }
		        },
                {
                    "type": "input",
                    "block_id": "day-block-id",
                    "element": {
                        "type": "datepicker",
                        "placeholder": { "type": "plain_text", "text": "日付を選択してください" },
                        "action_id": "day-action-id",
                    },
                    "label": { "type": "plain_text", "text": "開催日" }
                },
                {
			        "type": "input",
                    "block_id": "time-block-id",
			        "element": {
                        "type": "timepicker",
                        "initial_time": "12:00",
                        "placeholder": { "type": "plain_text", "text": "Select time" },
                        "action_id": "time-action-id",
			        },
			        "label": { "type": "plain_text", "text": "開始時刻" }
	    	    },
                {
                    "type": "input",
                    "block_id": "detail-block-id",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "detail-action-id",
                        "multiline": True,
                        "placeholder": { "type": "plain_text", "text": "できるだけ具体的に記入してください" }
                    },
                    "label": { "type": "plain_text", "text": "詳細内容" }
                }
            ]
        }
    )
    logger.info(res)    

# 「送信」ボタンが押されたときに呼び出されます
@app.view("modal-id")
# @app.view({"type": "view_closed", "callback_id": "modal-id"})
def handle_view_submission(ack, body, client, logger):
    ack()
    logger.info(body)
    channel = "#ハッカソン"
    values = body["view"]["state"]["values"]
    users = values["users-block-id"]["users-action-id"]["selected_users"]
    message = values["title-block-id"]["title-action-id"]["value"]
    time = values["time-block-id"]["time-action-id"]["selected_time"]
    place = values["place-block-id"]["place-action-id"]["selected_option"]["text"]["text"]
    day = values["day-block-id"]["day-action-id"]["selected_date"]
    detail = values["detail-block-id"]["detail-action-id"]["value"]

    # Slack API 上、他のユーザを直接通知するには、このようにユーザ ID を不等号に入れ、アットマークをつけると綺麗に表示されます <@user_id> 。
    at_users = " ".join([f"<@{name}>" for name in users])
    
    client.chat_postMessage(
        channel = channel,
        text = f"ユーザー：{at_users} \n {message} \n {time} \n {place} \n {day} \n {detail} "
    )


# アプリを起動します
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()