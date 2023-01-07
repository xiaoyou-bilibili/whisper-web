import time, threading

import whisper
from time import strftime, gmtime

import moviepy.editor as mp

model = whisper.load_model("large", download_root="./model")

process = ""
result = ""


def translate(audio_path: str):
    result = model.transcribe(audio_path)
    return result


# 提取音频文件
def video_extra(src, dst):
    my_clip = mp.VideoFileClip(src)
    my_clip.audio.write_audiofile(dst)


# 生成字幕文件
def generate_srt(data: list):
    text = ""
    for i in range(len(data)):
        item = data[i]
        text += "{}\n{} --> {}\n{}\n\n".format(i, strftime("%H:%M:%S", gmtime(item["start"])),
                                               strftime("%H:%M:%S", gmtime(item["end"])), item["text"])
    return text


class VideoThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, path):
        super().__init__()
        self._path = path

    def run(self):
        global process, result
        audio_path = "{}/tmp.mp3".format(self._path)
        process = "提取音频.."
        video_extra("{}/origin.mp4".format(self._path), audio_path)
        process = "识别中.."
        result = generate_srt(translate(audio_path)["segments"])
        process = "finish"


# 获取当前进度
def get_process():
    return {"process": process, "res": result}
