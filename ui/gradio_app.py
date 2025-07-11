import sys
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

import gradio as gr
import asyncio
from modules.asr_whisper import transcribe
from modules.chat_ollama import chat_with_ollama
from modules.tts_edge import speak
from modules.memory import add_to_memory
from modules.emotion import update_emotion_by_text, load_emotion


# 这个脚本所在的位置：ui/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# 它的上一级：项目根目录（即包含 modules/ 的地方）
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# 加入项目根目录作为模块导入路径
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("✅ 项目根路径已加入:", PROJECT_ROOT)

def get_emotion_image(emotion_state):
    max_emotion = max(emotion_state, key=emotion_state.get)
    emotion_map = {
        "依恋": "base.png",
        "幸福": "happy.png",
        "不安": "anxious.png",
        "悲伤": "sad.png"
    }
    return os.path.join("ui", "assets", emotion_map.get(max_emotion, "base.png"))

def respond(audio_path):
    user_text = transcribe(audio_path)

    user_text = transcribe("audio/input.wav")
    emotion = update_emotion_by_text(user_text)
    emotion_img = get_emotion_image(emotion)

    add_to_memory("user", user_text)
    ai_reply = chat_with_ollama("你叫晚音，是一个温柔的虚拟女伴。请用情绪化语气自然说话。", user_text)
    add_to_memory("assistant", ai_reply)

    asyncio.run(speak(ai_reply))
    os.system("start audio/output.mp3")

    return user_text, ai_reply, emotion_img

with gr.Blocks() as demo:
    gr.Markdown("## 🌙 晚音 - 可视化语音助手")

    with gr.Row():
        image = gr.Image(label="晚音当前状态", type="filepath", height=320, width=320)
        with gr.Column():
            user_textbox = gr.Textbox(label="你说了什么", lines=2)
            reply_textbox = gr.Textbox(label="晚音回应", lines=4)

    mic = gr.Audio(type="filepath", label="🎙️ 录音")

    submit_btn = gr.Button("开始和晚音对话")

    submit_btn.click(fn=respond, inputs=[mic], outputs=[user_textbox, reply_textbox, image])

demo.launch()
