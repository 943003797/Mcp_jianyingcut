import os, time
from mcp.server.fastmcp import FastMCP
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange

mcp = FastMCP("GetAudio")

@mcp.tool()
def get_time() -> str:
    """
    Use this tool to get current time.
    Parameters:
        None
    Returns:
        Success: return Success
        Failed: return Failed
    """
    testObj = Test()
    time = testObj.eh()
    print(time);
    return 'Success'

class Test:
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.a = int(time.time() * 1000)  # 获取当前时间戳，精确到毫秒
        
    def eh(self):
        print(self.a);