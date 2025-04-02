import pyJianYingDraft as draft
import json

try:
    draft_folder = draft.Draft_folder("S:/AI/AutoGenTest/output/JianyingPro Drafts")
    script = draft_folder.load_template("test")
    script.inspect_material()
except json.JSONDecodeError:
    print("错误：draft_content.json 文件为空或格式不正确，请检查文件内容。")
except FileNotFoundError:
    print("错误：draft_content.json 文件未找到，请检查文件路径。")
except Exception as e:
    print(f"发生未知错误：{e}")