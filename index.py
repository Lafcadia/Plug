from flask import Flask, request, send_from_directory
from os.path import dirname, abspath, join
from json import loads, dumps
import os
from core import search
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 3600  # 缓存时间为1小时
app.config['STATIC_FOLDER'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


@app.route('/')
def home():
    return send_from_directory(app.config['STATIC_FOLDER'], 'index.html')


@app.route('/s', methods=['GET'])
def about():
    try:
        content = []
        request_data, s = request.args.get('q'), request.args.get('s')
        if s in ["谷歌", "必应"]:
            if s == "谷歌":
                s = "google"
            elif s == "必应":
                s = "bing"
        result = search.search(request_data, s)
        for obj in result:
            try:
                content.append([obj.title, obj.summary, obj.url])
            except Exception as e:
                print(e)
                print(obj.title, obj.summary, obj.url)
    except Exception as e:
        return "Something's wrong. " + str(e), 500, {"Content-Type": "application/json"}
        # print(e)
        # return content, 200, {"Content-Type": "application/json"}
    return content, 200, {"Content-Type": "application/json"}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2333)
