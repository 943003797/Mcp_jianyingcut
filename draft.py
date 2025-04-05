import os, time, random
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange
from pyJianYingDraft import Text_intro, Text_outro, Text_loop_anim, Mask_type
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

    def __init__(self):
        self.DUMP_PATH = "../../AutoGenTest/output/JianyingPro Drafts/Draft/draft_content.json"
        self.tutorial_asset_dir = "../../AutoGenTest/output"
        self.script = draft.Script_file(1920, 1080)
        self.script.add_track(draft.Track_type.audio, 'TTS')
        self.script.add_track(draft.Track_type.audio, 'BGM')
        self.script.add_track(draft.Track_type.video, 'BGV', mute= True, relative_index=1)
        self.script.add_track(draft.Track_type.video, 'BGVC', mute= True, relative_index=0)
        self.script.add_track(draft.Track_type.sticker, 'STK')
        self.script.add_track(draft.Track_type.text, 'T0')
        self.script.add_track(draft.Track_type.text, 'T1')
        self.script.add_track(draft.Track_type.text, 'T2')
        self.script.add_track(draft.Track_type.text, 'T3')
        self.script.add_track(draft.Track_type.text, 'T4')
        self.script.add_track(draft.Track_type.text, 'T5')
        self.script.add_track(draft.Track_type.text, 'T6')
        self.script.add_track(draft.Track_type.text, 'ZZ')
        self.script.add_track(draft.Track_type.text, 'SX')
        self.script.add_track(draft.Track_type.text, 'SY')

    def addBgm(self, bgm: str):
        audio_bgm = draft.Audio_material(os.path.join(self.tutorial_asset_dir, bgm))
        audio_bgm_lenth = audio_bgm.duration
        self.script.add_material(audio_bgm)
        audio_bgm_segment = draft.Audio_segment(audio_bgm, trange(0, self.nowS),volume=0.2)
        audio_bgm_segment.add_fade("1s", "1s")
        self.script.add_segment(audio_bgm_segment, 'BGM')
        # 水印
        text_segment = draft.Text_segment("时间在走、", trange(0, self.nowS),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                    font=draft.Font_type.三极行楷简体_粗,                                  # 设置字体为文轩体
                                    style=draft.Text_style(color=(1, 1, 1)),                # 设置字体颜色为黄色
                                    border=draft.Text_border(alpha=0.2,color=(0, 0, 0)),
                                    clip_settings=draft.Clip_settings(transform_x=-0.85,transform_y=0.90, scale_x=0.45, scale_y=0.45))          # 模拟字幕的位置
        text_segment.add_animation(Text_intro.冰雪飘动, 1500000)
        text_segment.add_animation(Text_outro.渐隐, 500000)
        self.script.add_segment(text_segment, 'SY')
                # 诗词背景
        video_material = draft.Video_material(os.path.join(self.tutorial_asset_dir, "bgloop.mp4"))
        video_duration = video_material.duration
        self.script.add_material(video_material)
        video_segment = draft.Video_segment(material = video_material,
                                                        target_timerange  = trange(0, int(self.nowS) + 500000),
                                                        volume=0)
        self.script.add_segment(video_segment, 'BGVC')
        
    def addTitle(self, filename: str):
        audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, 't0.mp3'))
        audio_duration = audio_material.duration
        self.script.add_material(audio_material)
        audio_segment = draft.Audio_segment(audio_material,
                                    trange(self.nowS, audio_duration),
                                    volume=1)
        self.script.add_segment(audio_segment, 'TTS')
        self.nowS += audio_duration + 500000
        titleJson = os.path.join(self.tutorial_asset_dir, 'title.json')
        with open(titleJson, 'r', encoding='utf-8') as f:
            data = json.load(f)
            title = data.get('title')
        segments = [segment for segment in title.split('，') if segment]
        total_length = len(title)
        list = [[segment, round(len(segment) / total_length, 3)] for segment in segments]
        for key, (segment, ratio) in enumerate(list):
                    if key == 0:
                        start = 0
                        duration = audio_material.duration
                        animation_duration = ratio * audio_material.duration / 2
                        fixed_y = 0.2
                    else:
                        start = audio_material.duration * list[key-1][1]
                        duration = audio_material.duration * ratio
                        animation_duration = ratio * audio_material.duration / 4
                        fixed_y = -0.2
                    text_segment = draft.Text_segment(list[key][0], trange(start, duration),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                  font=draft.Font_type.三极行楷简体_粗,                                  # 设置字体为文轩体
                                  style=draft.Text_style(color=(1, 1, 1)),                # 设置字体颜色为黄色
                                  clip_settings=draft.Clip_settings(transform_y=fixed_y))          # 模拟字幕的位置
                    text_segment.add_animation(Text_intro.金粉飘落, animation_duration)
                    text_segment.add_animation(Text_outro.渐隐, animation_duration/2)
                    self.script.add_segment(text_segment, 'T' + str(key))
        video_material = draft.Video_material(os.path.join(self.tutorial_asset_dir, "bgv.mp4"))
        video_duration = video_material.duration
        self.script.add_material(video_material)
        video_segment = draft.Video_segment(video_material,
                                    trange(0, self.nowS),
                                    volume=0)
        self.script.add_segment(video_segment, 'BGV')
        
    
    def addItem(self, filename: str) -> str:
        with open(os.path.join(self.tutorial_asset_dir, f"{filename}.json"), 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for key, item in json_data.items() if isinstance(json_data, dict) else enumerate(json_data):
            # 音频素材
            itemPeiyinNow = self.nowS
            audio_duration = 0
            for i in range(10):
                if os.path.exists(os.path.join(self.tutorial_asset_dir, f"{item['peiyin']}{i}.mp3")):
                    audio_material = draft.Audio_material(os.path.join(self.tutorial_asset_dir, f"{item['peiyin']}{i}.mp3"))
                    audio_length = audio_material.duration
                    
                    self.script.add_material(audio_material)
                    audio_segment = draft.Audio_segment(audio_material,
                                    trange(int(itemPeiyinNow), int(audio_length)),
                                    volume=1)
                    self.script.add_segment(audio_segment, 'TTS')
                    itemPeiyinNow += audio_length
                    audio_duration+=audio_length
            
            # 背景素材,分段定制
            
            # video_material = draft.Video_material(os.path.join(self.tutorial_asset_dir, "bgloop.mp4"))
            # video_duration = video_material.duration
            # self.script.add_material(video_material)
            # video_segment = draft.Video_segment(material = video_material,
            #                                             target_timerange  = trange(int(self.nowS), int(audio_duration) + 500000),
            #                                             source_timerange = trange(f"{random.randint(110,240)}s", int(audio_duration)),
            #                                             volume=0)
            # self.script.add_segment(video_segment, 'BGV')

            Sticker_segment = draft.Sticker_segment(
                resource_id = "7226264888031694091",
                target_timerange = trange(int(self.nowS), int(audio_duration) + 500000),
                clip_settings = draft.Clip_settings(
                    scale_x = 2,
                    scale_y = 0.25
                )
            )
            self.script.add_segment(Sticker_segment, 'STK')
            # 字幕素材
            title = item['shiJuSplit']
            segments = [segment for segment in title.split('|') if segment]
            total_length = len(title)
            list = [[segment, round(len(segment) / total_length, 3)] for segment in segments]
            splitNum = len(list) - 1
            split = [
                {
                    "fixed": [
                        [-0.5,0.5]
                    ]
                },
                {
                    "fixed": [
                        [-0.3,0.15],
                        [0.3,-0.15]
                    ]
                },
                {
                    "fixed": [
                        [0,0.2],
                        [0,0],
                        [0,-0.2]
                    ]
                },
                {
                    "fixed": [
                        [-0.4,0.15],
                        [0.4,0.15],
                        [-0.4,-0.15],
                        [0.4,-0.15]
                    ]
                }
            ]
            # 作者信息
            text_segment = draft.Text_segment(f"——{item['zuoZhe']}《{item['shiMing']}》", trange(self.nowS, int(audio_duration)),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                    font=draft.Font_type.三极行楷简体_粗,                                  # 设置字体为文轩体
                                    style=draft.Text_style(color=(1, 1, 1)),                # 设置字体颜色为黄色
                                    border=draft.Text_border(color=(0, 0, 0)),
                                    clip_settings=draft.Clip_settings(transform_y=-0.7, scale_x=0.45, scale_y=0.45))          # 模拟字幕的位置
            text_segment.add_animation(Text_intro.渐显, 500000)
            text_segment.add_animation(Text_outro.渐隐, 500000)
            self.script.add_segment(text_segment, 'ZZ')
            # 赏析
            text_segment = draft.Text_segment(f"{item['shangXi']}", trange(self.nowS, int(audio_duration)),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                    font=draft.Font_type.三极行楷简体_粗,                                  # 设置字体为文轩体
                                    style=draft.Text_style(color=(1, 1, 1)),                # 设置字体颜色为黄色
                                    border=draft.Text_border(color=(0, 0, 0)),
                                    clip_settings=draft.Clip_settings(transform_y=-0.85, scale_x=0.45, scale_y=0.45))          # 模拟字幕的位置
            text_segment.add_animation(Text_intro.渐显, 500000)
            text_segment.add_animation(Text_outro.渐隐, 500000)
            self.script.add_segment(text_segment, 'SX')
            indent = 500000
            for key, item in enumerate(list):
                        if key == 0:
                            start = self.nowS
                            duration = audio_duration
                            animation_duration = audio_duration / 4
                            fixed_x = split[splitNum]['fixed'][key][0]
                            fixed_y = split[splitNum]['fixed'][key][1]
                        else:
                            start = self.nowS + indent
                            duration = self.nowS + audio_duration - start
                            animation_duration = audio_duration / 4
                            fixed_x = split[splitNum]['fixed'][key][0]
                            fixed_y = split[splitNum]['fixed'][key][1]
                        text_segment = draft.Text_segment(list[key][0], trange(start, duration),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                    font=draft.Font_type.三极行楷简体_粗,                                  # 设置字体为文轩体
                                    style=draft.Text_style(color=(1, 1, 1)),                # 设置字体颜色为黄色
                                    clip_settings=draft.Clip_settings(transform_x=fixed_x, transform_y=fixed_y))          # 模拟字幕的位置
                        text_segment.add_animation(Text_intro.冰雪飘动, animation_duration)
                        text_segment.add_animation(Text_outro.渐隐, animation_duration/3)
                        self.script.add_segment(text_segment, 'T' + str(key))
                        indent += 500000
            print(audio_duration/500000)
            self.nowS += audio_duration + 500000
        return 'Success'
    
    def addVideo(self, filename: str):
        video_material = draft.Video_material(os.path.join(self.tutorial_asset_dir, filename))
        video_duration = video_material.duration
        self.script.add_material(video_material)
        video_segment = draft.Video_segment(video_material,
                                    trange(0, self.nowS),
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
    testObj = Test()
    testObj.addTitle('title')
    testObj.addItem('item')
    testObj.addBgm('BGM_爱的供养_间奏.mp3')
    # testObj.addVideo('bgv.mp4')
    testObj.dumpDraft()