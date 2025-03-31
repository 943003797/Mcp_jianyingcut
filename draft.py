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
        self.DUMP_PATH = "S:/AI/AutoGenTest/output/JianyingPro Drafts/acc/draft_content.json"
        #素材路径
        self.tutorial_asset_dir = os.path.join(os.path.dirname(__file__), 'readme_assets', 'tutorial')
        assert os.path.exists(self.tutorial_asset_dir), f"未找到例程素材文件夹{os.path.abspath(self.tutorial_asset_dir)}"
        # self.tutorial_asset_dir = "S:/AI/AutoGenTest/output"
        # self.tutorial_asset_dir = os.path.join('C:Users/Kinso/Documents/AI/AutoGenTest/Agent', 'readme_assets', 'tutorial')
        #创建草稿
        self.script = draft.Script_file(1920, 1080)
    
    def addAudio(self, filename: str) -> str:
        # self.script.add_track(draft.Track_type.video).add_track(draft.Track_type.text)
        # 添加音频轨道
        # self.script.add_track(draft.Track_type.audio, track_name="audio0", relative_index=0)
        self.script.add_track(draft.Track_type.audio, '1').add_track(draft.Track_type.video).add_track(draft.Track_type.text)
        
        # 使用 draft.Audio_material 获取音频文件
        audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, 'a.mp3'))
        # 获取音频时长
        # audio_duration = audio_material.duration/1000000
        # audio_segment = draft.Audio_segment(audio_material,
        #                             trange(self.nowS, round(float(audio_duration), 1)),
        #                             volume=1)
        audio_segment = draft.Audio_segment(audio_material, trange("0s", "3s"))
        # audio_segment.add_fade("1s", "0s")
        self.script.add_segment(audio_segment, '1')
        # self.nowS += audio_duration

        text_segment = draft.Text_segment("据说pyJianYingDraft效果还不错?", trange(0, self.script.duration),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                  font=draft.Font_type.文轩体,                                  # 设置字体为文轩体
                                  style=draft.Text_style(color=(1.0, 1.0, 0.0)),                # 设置字体颜色为黄色
                                  clip_settings=draft.Clip_settings(transform_y=-0.8))          # 模拟字幕的位置
        self.script.add_segment(text_segment)




        self.script.dump(self.DUMP_PATH)
        return 'Success'

    # def addText(self):
    #     self.script.add_track(draft.Track_type.text, track_name="text0", relative_index=0)
        
    # def addAllAudio(self):
    #     # 遍历音频文件夹中的所有文件
    #     for filename in os.listdir(self.tutorial_asset_dir):
    #         # 检查文件是否为音频文件
    #         if filename.endswith(('.mp3', '.wav', '.m4a')):
    #             self.addAudio(filename)
if __name__ == "__main__":
    testObj = Test()
    testObj.addAudio('b.mp3')