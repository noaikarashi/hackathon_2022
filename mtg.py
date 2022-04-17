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
                        "action_id": "input",
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
                        "action_id": "input",
                        "placeholder": { "type": "plain_text", "text": "ミーティングに参加するユーザを選択してください", "emoji": True}
                    },
                    "label": { "type": "plain_text", "text": "参加者", "emoji": True},
                    "optional": True
                },
                {
		        	"type": "input",
			        "element": {
                        "type": "static_select",
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
	    			],
		    	    "action_id": "static_select-action"
			        },
			        "label": { "type": "plain_text", "text": "活動場所", "emoji": True }
		        },
                {
                    "type": "input",
                    "block_id": "input-deadline",
                    "element": {
                        "type": "datepicker",
                        "action_id": "input",
                        "placeholder": { "type": "plain_text", "text": "日付を選択してください", "emoji": True }
                    },
                    "label": { "type": "plain_text", "text": "開催日", "emoji": True },
                    "optional": True
                },
                {
			        "type": "input",
			        "element": {
                        "type": "timepicker",
                        "initial_time": "12:00",
                        "placeholder": { "type": "plain_text", "text": "Select time", "emoji": True },
		    		"action_id": "timepicker-action"
			        },
			        "label": { "type": "plain_text", "text": "開始時刻", "emoji": True }
	    	    },
                {
                    "type": "input",
                    "block_id": "input-description",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input",
                        "multiline": True,
                        "placeholder": { "type": "plain_text", "text": "できるだけ具体的に記入してください", "emoji": True }
                    },
                    "label": { "type": "plain_text", "text": "詳細内容", "emoji": True },
                    "optional": True
                }
            ]
        }
    )

        # ユーザがモーダルからデータ送信したときのリスナーです
@app.view("modal-id")
def view_submission(ack: Ack, body: dict, client: WebClient, logger):
    ack()
    logger.info(body)
    # チャンネル ID を指定することもできます
    client.chat_postMessage(
        channel= "#ハッカソン",
        blocks= [
                {   
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": dict['input-title']                #"You have a new request:\n*<google.com|Fred Enriquez - Time Off request>*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Type:*\nPaid time off\n*When:*\nAug 10-Aug 13\n*Hours:* 16.0 (2 days)\n*Remaining balance:* 32.0 hours (4 days)\n*Comments:* \"Family in town, going camping!\""
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/approvalsNewDevice.png",
                        "alt_text": "computer thumbnail"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Approve"
                            },
                            "style": "primary",
                            "value": "click_me_123"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Deny"
                            },
                            "style": "danger",
                            "value": "click_me_123"
                        }
                    ]
                }
            ]
    )


# アプリを起動します
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()