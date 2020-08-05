from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('dkh+McW66jN49zhnAc2g7R7oHNdsD3fJOBnpbbSCdwq7iHL1xPm17Q500SKWnj9UgobhZSJw2fd9UmCDzhID0LsGTZ3Lmr7lZd+4Wi1ludDYjEvKo/SuW/fI1uvIM/KDXuCwb8mYGwJ/Pcw2yNLJlAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d0f36aa8ad11d8eb58956569fdfd4022')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()