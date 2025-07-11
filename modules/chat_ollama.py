import requests
from modules.memory import load_memory
from modules.emotion import load_emotion

def chat_with_ollama(prompt, user_input, model="EntropyYue/chatglm3:6b"):
    memory = load_memory()
    emotion = load_emotion()
    
    emotion_desc = f"""
当前情绪状态如下：
依恋度：{round(emotion['依恋']*100)}%
不安感：{round(emotion['不安']*100)}%
幸福感：{round(emotion['幸福']*100)}%
悲伤感：{round(emotion['悲伤']*100)}%
请根据这些状态，改变你的语气和行为，越高的情绪应越明显表达。
"""

    history = "\n".join([f"{'她' if m['role']=='user' else '你'}：{m['content']}" for m in memory])
    
    full_prompt = f"{prompt}\n\n{emotion_desc}\n\n以下是你们的对话历史：\n{history}\n\n她：{user_input}\n你："

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            }
        )
        data = response.json()

        if "response" in data:
            return data["response"].strip()
        elif "error" in data:
            return f"（出错了：{data['error']}）"
        else:
            return "(没有返回内容，请检查模型是否正常启动)"
    except Exception as e:
        return f"(请求失败：{str(e)})"
