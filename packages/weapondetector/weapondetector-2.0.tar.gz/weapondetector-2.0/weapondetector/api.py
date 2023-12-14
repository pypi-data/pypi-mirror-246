
from waitress import serve
from flask import Flask, request
import json
import threading

from utils import uploading_thread


app = Flask(__name__)


@app.route('/uploadvideo', methods=['POST'])
def uploadvideo():
    if request.method == 'POST':
        data = json.loads(request.json)

        print(data)
        thread = threading.Thread(target=uploading_thread, args=(data['video_file_path'],
                                                                 data['img_file_path'],
                                                                 data['camera_name'],
                                                                 data['acc']))
        thread.daemon = True
        thread.start()
        thread.join()
        return data, 200


if __name__ == "__main__":

    serve(app, host="0.0.0.0", port=8000)
