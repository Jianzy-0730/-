import sounddevice as sd
import soundfile as sf
from modules.asr_whisper import transcribe
from modules.chat_ollama import chat_with_ollama
from modules.tts_edge import speak
from modules.config import SYSTEM_PROMPT
import asyncio
import os
from modules.memory import add_to_memory
from modules.emotion import update_emotion_by_text, format_emotion



def record_audio(filename, duration=5):
    print("🎤 开始录音...")
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, recording, fs)
    print("✅ 录音完成")

if __name__ == "__main__":
    record_audio("audio/input.wav")
    user_text = transcribe("audio/input.wav")
    add_to_memory("user", user_text)
    emotion = update_emotion_by_text(user_text)

    print("你说：", user_text)
    print("当前情绪状态：", format_emotion(emotion))
    ai_reply = chat_with_ollama(SYSTEM_PROMPT, user_text)
    add_to_memory("assistant", ai_reply)
    print("晚音：", ai_reply)
    
    asyncio.run(speak(ai_reply))
    os.system("start audio/output.mp3")
