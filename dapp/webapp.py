from tempfile import NamedTemporaryFile

import time
from flask import Flask, render_template, send_from_directory, request, send_file, stream_with_context, Response

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    name = NamedTemporaryFile(delete=False).name
    print("Saved: {}".format(name))
    request.files['image_file'].save(name)

    def generate():
        yield 'id: 123'
        time.sleep(2)
        yield 'data: hello'
        time.sleep(10)
        yield 'data: {}'.format(name)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
