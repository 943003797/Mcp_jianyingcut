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

    def __init__(self):
        #草稿路径
        self.DUMP_PATH = r"test/draft_content.json"
        #素材路径
        self.tutorial_asset_dir = "C:/Users/Kinso/Documents/AI/AutoGenTest/Agent/readme_assets/tutorial"
        # self.tutorial_asset_dir = os.path.join('C:Users/Kinso/Documents/AI/AutoGenTest/Agent', 'readme_assets', 'tutorial')
        #创建草稿
        self.script = draft.Script_file(1920, 1080)

    def addText(self):
        self.script.add_track(draft.Track_type.text, track_name="text0", relative_index=0)
        
    def addAllAudio(self):
        # 遍历音频文件夹中的所有文件
        for filename in os.listdir(self.tutorial_asset_dir):
            # 检查文件是否为音频文件
            if filename.endswith(('.mp3', '.wav', '.m4a')):
                self.addAudio(filename)
        
    def addAudio(self, filename: str) -> str:
        self.script.add_track(draft.Track_type.video).add_track(draft.Track_type.text)
        # 添加音频轨道
        self.script.add_track(draft.Track_type.audio, track_name="audio0", relative_index=0)
        
        # 使用 draft.Audio_material 获取音频文件
        path = self.tutorial_asset_dir
        # 修复点：使用传入的filename参数代替硬编码的'a.mp3'
        audio_material = draft.Audio_material(filename)# 修改此行
        # 获取音频时长
        audio_duration = audio_material.duration/1000000
        audio_segment = draft.Audio_segment(audio_material,
                                    trange(self.nowS, round(float(audio_duration), 1)),
                                    volume=1)
        audio_segment.add_fade("1s", "0s")
        self.nowS += audio_duration
        self.script.add_segment(audio_segment)
        self.script.dump(self.DUMP_PATH)
        return 'Success'
if __name__ == "__main__":
    testObj = Test()
    testObj.addAudio('a.mp3')