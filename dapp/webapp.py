import logging
from tempfile import NamedTemporaryFile

import ipfsapi
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Change according to your ipfs node setting
api = ipfsapi.connect('localhost', 5001)

logger = app.logger
logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


def validate_voice(voice):

    # Add voice validation with zeroth
    return True


@app.route('/upload', methods=['POST'])
def upload():
    name = NamedTemporaryFile(delete=False).name
    logger.info("Saved: {}".format(name))
    request.files['voice_file'].save(name)

    # Validate_voice
    if validate_voice(name):  # Validated
        # earn token
        pass

    else:  # Failed
        # ignore
        pass

    # Upload voice
    hash_value = api.add(name)['Hash']

    local_url = "http://localhost:8080/ipfs/{}".format(hash_value)
    ipfsio_url = "https://ipfs.io/ipfs/{}".format(hash_value)

    return "<a href={}>{}</a><br><a href={}>{}</a>".format(local_url, local_url, ipfsio_url, ipfsio_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
