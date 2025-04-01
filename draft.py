import os, time
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange

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
        self.script.add_track(draft.Track_type.text, 'T0')
        
        audio_bgm = draft.Audio_material(os.path.join(self.tutorial_asset_dir, bgm))
        audio_bgm_lenth = audio_bgm.duration/1000000
        self.script.add_material(audio_bgm)
        audio_bgm_segment = draft.Audio_segment(audio_bgm, trange(f"{self.nowS}s", f"{audio_bgm_lenth}s"),volume=0.2)
        audio_bgm_segment.add_fade("1s", "1s")
        self.script.add_segment(audio_bgm_segment, 'BGM')
        
    def addTitle(self, filename: str):
        audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, f'{filename}.mp3'))
        audio_duration = audio_material.duration/1000000
        self.script.add_material(audio_material)
        audio_segment = draft.Audio_segment(audio_material,
                                    trange(f"{self.nowS}s", f"{audio_duration}s"),
                                    volume=1)
        self.script.add_segment(audio_segment, 'TTS')
        self.nowS += audio_duration + 0.3
        #字幕
        text_segment = draft.Text_segment("千古词帝，李煜的巅峰之作", trange(0, self.script.duration),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                  font=draft.Font_type.文轩体,                                  # 设置字体为文轩体
                                  style=draft.Text_style(color=(1.0, 1.0, 0.0)),                # 设置字体颜色为黄色
                                  clip_settings=draft.Clip_settings(transform_y=-0.8))          # 模拟字幕的位置
        self.script.add_segment(text_segment, 'T0')
        
    
    def addItem(self, filename: str) -> str:
        # 音频
        audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, f'{filename}.mp3'))
        audio_duration = audio_material.duration/1000000
        self.script.add_material(audio_material)
        audio_segment = draft.Audio_segment(audio_material,
                                    trange(f"{self.nowS}s", f"{audio_duration}s"),
                                    volume=1)
        self.script.add_segment(audio_segment, 'TTS')
        self.nowS += audio_duration + 0.3
        # 字幕
        
        return 'Success'

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
    testObj.addTitle('t0')
    testObj.addItem('t1')
    testObj.addItem('t2')
    testObj.addItem('t3')
    testObj.addItem('t4')
    testObj.addItem('t5')
    testObj.addItem('t6')
    testObj.addItem('t7')
    testObj.dumpDraft()