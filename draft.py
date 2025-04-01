import os, time
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange
from pyJianYingDraft import Text_intro, Text_outro, Text_loop_anim
from pyJianYingDraft import animation
from pyJianYingDraft.script_file import json

class Test:
    _instance = None
    script = draft.Script_file(1920, 1080)
    tutorial_asset_dir = ""
    nowS = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self, bgm: str = "bgm.mp3"):
        self.DUMP_PATH = "../../AutoGenTest/output/JianyingPro Drafts/Draft/draft_content.json"
        self.tutorial_asset_dir = "../../AutoGenTest/output"
        self.script = draft.Script_file(1920, 1080)
        self.script.add_track(draft.Track_type.audio, 'TTS')
        self.script.add_track(draft.Track_type.audio, 'BGM')
        self.script.add_track(draft.Track_type.video, 'BGV')
        self.script.add_track(draft.Track_type.text, 'T0')
        self.script.add_track(draft.Track_type.text, 'T1')
        self.script.add_track(draft.Track_type.text, 'T2')
        self.script.add_track(draft.Track_type.text, 'T3')
        self.script.add_track(draft.Track_type.text, 'T4')
        self.script.add_track(draft.Track_type.text, 'T5')
        self.script.add_track(draft.Track_type.text, 'T6')
        self.script.add_track(draft.Track_type.text, 'ZZ')
        self.script.add_track(draft.Track_type.text, 'SX')
        
        audio_bgm = draft.Audio_material(os.path.join(self.tutorial_asset_dir, bgm))
        audio_bgm_lenth = audio_bgm.duration
        self.script.add_material(audio_bgm)
        audio_bgm_segment = draft.Audio_segment(audio_bgm, trange(self.nowS, audio_bgm_lenth),volume=0.2)
        audio_bgm_segment.add_fade("1s", "1s")
        self.script.add_segment(audio_bgm_segment, 'BGM')
        
    def addTitle(self, filename: str):
        audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, f'{filename}.mp3'))
        audio_duration = audio_material.duration
        self.script.add_material(audio_material)
        audio_segment = draft.Audio_segment(audio_material,
                                    trange(self.nowS, audio_duration),
                                    volume=1)
        self.script.add_segment(audio_segment, 'TTS')
        self.nowS += audio_duration + 500000
        title = "千古词帝，李煜的巅峰之作。哪句更触动你心"
        segments = [segment for segment in title.split('。') if segment]
        total_length = len(title)
        list = [[segment, round(len(segment) / total_length, 3)] for segment in segments]
        for key, (segment, ratio) in enumerate(list):
                    if key == 0:
                        start = 0
                        duration = audio_material.duration
                        animation_duration = ratio * audio_material.duration / 4
                        fixed_y = 0.2
                    else:
                        start = audio_material.duration * list[key-1][1]
                        duration = audio_material.duration * ratio
                        animation_duration = ratio * audio_material.duration / 4
                        fixed_y = -0.2
                    text_segment = draft.Text_segment(list[key][0], trange(start, duration),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                  font=draft.Font_type.文轩体,                                  # 设置字体为文轩体
                                  style=draft.Text_style(color=(0.9, 0.9, 0.9)),                # 设置字体颜色为黄色
                                  clip_settings=draft.Clip_settings(transform_y=fixed_y))          # 模拟字幕的位置
                    text_segment.add_animation(Text_intro.冰雪飘动, animation_duration)
                    text_segment.add_animation(Text_outro.渐隐, animation_duration)
                    self.script.add_segment(text_segment, 'T' + str(key))
        
    
    def addItem(self, filename: str) -> str:
        with open(os.path.join(self.tutorial_asset_dir, f"{filename}.json"), 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for key, item in json_data.items() if isinstance(json_data, dict) else enumerate(json_data):
            # 音频素材
            audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, f"{item['ttsName']}.mp3"))
            audio_duration = audio_material.duration
            print(audio_duration)
            self.script.add_material(audio_material)
            audio_segment = draft.Audio_segment(audio_material,
                                    trange(int(self.nowS), int(audio_duration)),
                                    volume=1)
            self.script.add_segment(audio_segment, 'TTS')
            # 字幕素材
            title = item['shiJuSplit']
            segments = [segment for segment in title.split('|') if segment]
            total_length = len(title)
            list = [[segment, round(len(segment) / total_length, 3)] for segment in segments]
            print(list)
            splitNum = len(list) - 1
            split = [
                {
                    "fixed": [0.5]
                },
                {
                    "fixed": [0.15,-0.15]
                },
                {
                    "fixed": [0.3,0,-0.3]
                },
                {
                    "fixed": [0.35,0.125,-0.125,-0.35]
                }
            ]
            # 作者信息
            text_segment = draft.Text_segment(f"——{item['zuoZhe']}《{item['shiMing']}》", trange(self.nowS, int(audio_duration)),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                    font=draft.Font_type.文轩体,                                  # 设置字体为文轩体
                                    style=draft.Text_style(color=(0.9, 0.9, 0.9)),                # 设置字体颜色为黄色
                                    clip_settings=draft.Clip_settings(transform_y=-0.7, scale_x=0.5, scale_y=0.5))          # 模拟字幕的位置
            text_segment.add_animation(Text_intro.渐显, 500000)
            text_segment.add_animation(Text_outro.渐隐, 500000)
            self.script.add_segment(text_segment, 'ZZ')
            # 赏析
            text_segment = draft.Text_segment(f"{item['shangXi']}", trange(self.nowS, int(audio_duration)),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                    font=draft.Font_type.文轩体,                                  # 设置字体为文轩体
                                    style=draft.Text_style(color=(0.9, 0.9, 0.9)),                # 设置字体颜色为黄色
                                    clip_settings=draft.Clip_settings(transform_y=-0.9, scale_x=0.5, scale_y=0.5))          # 模拟字幕的位置
            text_segment.add_animation(Text_intro.渐显, 500000)
            text_segment.add_animation(Text_outro.渐隐, 500000)
            self.script.add_segment(text_segment, 'SX')
            indent = 500000
            for key, item in enumerate(list):
                        if key == 0:
                            start = self.nowS
                            duration = audio_material.duration
                            animation_duration = audio_material.duration / 4
                            fixed_y = split[splitNum]['fixed'][key]
                        else:
                            start = self.nowS + indent
                            # print(self.nowS + audio_material.duration)
                            # print(start)
                            # print(self.nowS + audio_material.duration - start)
                            duration = self.nowS + audio_material.duration - start
                            animation_duration = audio_material.duration / 4
                            fixed_y = split[splitNum]['fixed'][key]
                        text_segment = draft.Text_segment(list[key][0], trange(start, duration),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                    font=draft.Font_type.文轩体,                                  # 设置字体为文轩体
                                    style=draft.Text_style(color=(0.9, 0.9, 0.9)),                # 设置字体颜色为黄色
                                    clip_settings=draft.Clip_settings(transform_y=fixed_y))          # 模拟字幕的位置
                        text_segment.add_animation(Text_intro.冰雪飘动, animation_duration)
                        text_segment.add_animation(Text_outro.渐隐, animation_duration/3)
                        self.script.add_segment(text_segment, 'T' + str(key))
                        indent += 500000
            self.nowS += audio_duration + 500000
        return 'Success'
    
    def addVideo(self, filename: str):
        video_material = draft.Video_material(os.path.join(self.tutorial_asset_dir, filename))
        video_duration = video_material.duration
        self.script.add_material(video_material)
        video_segment = draft.Video_segment(video_material,
                                    trange(0, video_duration),
                                    volume=0)
        self.script.add_segment(video_segment, 'BGV')

    def dumpDraft(self):
        self.script.dump(self.DUMP_PATH)

    # def addText(self):
    #     self.script.add_track(draft.Track_type.text, track_name="text0", relative_index=0)
        
    # def addAllAudio(self):
    #     # 遍历音频文件夹中的所有文件
    #     for filename in os.listdir(self.tutorial_asset_dir):
    #         # 检查文件是否为音频文件
    #         if filename.endswith(('.mp3', '.wav', '.m4a')):
    #             self.addAudio(filename)
if __name__ == "__main__":
    testObj = Test('爱的供养-间奏.mp3')
    testObj.addVideo('bgv.mp4')
    testObj.addTitle('t0')
    testObj.addItem('item')
    testObj.dumpDraft()