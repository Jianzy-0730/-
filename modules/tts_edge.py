import edge_tts
import asyncio

async def speak(text):
    communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural", rate="-5%")
    await communicate.save("audio/output.mp3")
