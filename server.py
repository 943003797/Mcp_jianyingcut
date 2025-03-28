import os
from mcp.server.fastmcp import FastMCP
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange

mcp = FastMCP("GetAudio")

script = 

@mcp.tool()
def create_draft(width: int = 1920, height: int = 1080) -> str:
    """
    Use this tool to create a draft. Input width and height to create a draft.
    Parameters:
        width: Width of the draft
        height: Height of the draft
    Returns:
        Success: return Success
        Failed: return Failed
    """
    
    try:
        script = draft.Script_file(width, height)
        script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)
        return "Success"
    except Exception as e:
        print(f"Error: {e}")
    return "Failed"

@mcp.tool()
def add_segment(text: str = 'undefind segment', start: str = '0s', duration: str = '0.1s', x: float = 0.0, y: float = 0.0) -> str:
    """
    Use this tool to add a text segment to the draft. Input text and start time to add a text segment to the draft.
    Parameters:
        text: Text to add
        start: Start time of the segment
        duration: Duration of the segment
        x: X position of the segment
        y: Y position of the segment
    Returns:
        Success: Operation successful
        Failed: Operation failed
    """
    script.add_track(draft.Track_type.text)

@mcp.tool()
def create_text_to_audio(text: str,file_neme: str, file_path: str) -> str:
    """
    Use this tool to generate voiceover. Input text and directory to generate and save voiceover to the specified directory
    Parameters:
        text: Text to generate voiceover from
        file_neme: File name
        file_path: Save directory
    Returns:
        Success: Operation successful
        Failed: Operation failed
    """

    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    # url = "https://api.hostize.com/files/d7B0_pGfZZ/download/file.wav"
    # prefix = 'prefix'
    target_model = "cosyvoice-v1"

    service = VoiceEnrollmentService()

    voice_id = "cosyvoice-prefix-4eec46a3b5d8499a8c29c46766452a63"
    synthesizer = SpeechSynthesizer(model=target_model, voice=voice_id)
    audio_result = synthesizer.call(text)
    print("requestId: ", synthesizer.get_last_request_id())

    save_directory = file_path if file_path else ""
    os.makedirs(save_directory, exist_ok=True)
    file_path = os.path.join(save_directory, f"{file_neme}.mp3")
    try:
        with open(file_path, "wb") as f:
            f.write(audio_result)
        return "Success"
    except Exception as e:
        print(f"Error: {e}")
        return "Failed"

if __name__ == "__main__":
    mcp.run(transport='stdio')