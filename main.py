from flask import Flask
from flask import request
from flask import Response

from commands import *
from tg_utils import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)

        message = Message(msg)
        txt = message.text()
        if txt is None:
            process_content(message)
            return Response('ok', status=200)

        result = process_command(message)
        if not result:
            process_random_choice(message)

        return Response('ok', status=200)

    else:
        return "<p>Hey buddy, I think you've got the wrong door</p>"


if __name__ == '__main__':
    app.run(debug=True)
