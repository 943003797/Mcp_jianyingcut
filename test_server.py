import os, time
from mcp.server.fastmcp import FastMCP
# import pyJianYingDraft as draft
# from pyJianYingDraft import Intro_type, Transition_type, trange

mcp = FastMCP("GetAudioo")

class Test:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'a'):
            self.a = int(time.time() * 1000)  # 获取当前时间戳，精确到毫秒

    def eh(self):
        return self.a

@mcp.tool()
def get_cc_value() -> str:
        """
        Use this tool to get cc value.
        Parameters:
            None
        Returns:
            Success: return cc value
            Failed: return Failed
        """
        testObj = Test()
        timex = testObj.eh()
        return str(timex)
    
@mcp.tool()
def get_dd_value() -> str:
        """
        Use this tool to get dd value.
        Parameters:
            None
        Returns:
            Success: return dd value
            Failed: return Failed
        """
        testObjd = Test()
        timed = testObjd.eh()
        return str(timed)

if __name__ == "__main__":
    mcp.run(transport='stdio')