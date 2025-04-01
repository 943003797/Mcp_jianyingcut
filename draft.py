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
        audio_bgm = draft.Audio_material(os.path.join(self.tutorial_asset_dir, bgm))
        audio_bgm_lenth = audio_bgm.duration/1000000
        self.script.add_material(audio_bgm)
        audio_bgm_segment = draft.Audio_segment(audio_bgm, trange(f"{self.nowS}s", f"{audio_bgm_lenth}s"),volume=0.2)
        audio_bgm_segment.add_fade("1s", "1s")
        self.script.add_segment(audio_bgm_segment, 'BGM')
        
    def addTitle(self, filename: str):
        audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, 'title.mp3'))
        audio_duration = audio_material.duration/1000000
        self.script.add_material(audio_material)
        audio_segment = draft.Audio_segment(audio_material,
                                    trange(f"{self.nowS}s", f"{audio_duration}s"),
                                    volume=1)
        self.script.add_segment(audio_segment, 'TTS')
        self.nowS += audio_duration + 0.3
        
    
    def addItem(self, filename: str) -> str:
        audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, filename))
        audio_duration = audio_material.duration/1000000
        self.script.add_material(audio_material)
        audio_segment = draft.Audio_segment(audio_material,
                                    trange(f"{self.nowS}s", f"{audio_duration}s"),
                                    volume=1)
        self.script.add_segment(audio_segment, 'TTS')
        self.nowS += audio_duration + 0.3
        
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
    testObj.addTitle('title.mp3')
    testObj.addItem('a.mp3')
    testObj.addItem('b.mp3')
    testObj.dumpDraft()