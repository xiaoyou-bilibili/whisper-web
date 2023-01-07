import base64

from flask import Flask, request, Response, render_template
import json, threading

from core import VideoThread, get_process, translate

# 初始化flaskAPP
app = Flask(__name__)


# 返回JSON字符串
def return_json(data):
    with open("tmp.json", "w") as f:
        f.write(json.dumps(data, ensure_ascii=False))
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 音色转换
@app.route('/whisper/trans', methods=['POST'])
def clone_voice1():
    audio = request.form.get('audio')
    # 直接把音频信息保存为文件
    path = "./web/static/origin.wav"
    audio = audio.replace("data:audio/wav;base64,", "")
    with open(path, "wb") as f:
        f.write(base64.b64decode(audio))
    # 返回json类型字符串
    return return_json({
        'origin': '/static/origin.wav',
        'translate': translate(path)
    })


# 音色转换
@app.route('/whisper/video', methods=['POST'])
def clone_voice2():
    f = request.files["video"]
    path = "./web/static"
    f.save("{}/origin.mp4".format(path))
    VideoThread(path).start()
    # 返回json类型字符串
    return return_json({})


# 获取视频的处理进度
@app.route('/whisper/process', methods=['GET'])
def clone_voice3():
    # 返回json类型字符串
    return return_json(get_process())


# 主页显示HTML
@app.route('/', methods=['GET'])
def index():
    return render_template('content.html')
