import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# ボットトークンと署名シークレットを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# アプリが参加しているチャンネルのメッセージイベントのリスナー
# channels:history scope を追加して bot user をチャンネルに invite しておく必要があります
@app.event("message")
def events(body: dict, say: Say, context: BoltContext):
    # 常に存在しません
    assert body.get("response_url") is None

    # また Events API の場合は ack() を Bolt 側が自動で行う & もし手動で呼べたとしても
    # 常にチャンネルに紐づいたイベントとも限らないので ack() に text を渡して返信するといったことは
    # Bolt の仕様・実装の制約ではなく、仕組み上できません

    if context.channel_id:
        # もしチャンネルに紐づいているイベントであれば context.channel_id が存在しているはずで
        # その場合は say 関数（chat.postMessage のラッパーです）にそのチャンネルが自動で設定されています
        # （message event の場合は必ず say が使えますが、他の event の場合は常にそうとは限りません）
        say(f"<@{context.user_id}> さん！このメッセージは `say()` を使って送信しました。")



# アプリを起動します
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()