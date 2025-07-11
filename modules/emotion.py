import json
import os

EMOTION_FILE = "emotion_state.json"

# 初始状态
DEFAULT_EMOTION = {
    "依恋": 0.5,
    "不安": 0.3,
    "幸福": 0.4,
    "悲伤": 0.2
}

# 情绪关键词：你可以自定义加强她的敏感面~
TRIGGERS = {
    "我不在": {"不安": 0.3, "悲伤": 0.2},
    "想你": {"依恋": 0.4, "幸福": 0.2},
    "你在吗": {"依恋": 0.3, "不安": 0.2},
    "不理我": {"不安": 0.5, "悲伤": 0.3},
    "晚音": {"依恋": 0.2},
    "抱抱": {"幸福": 0.4, "依恋": 0.3},
    "走开": {"悲伤": 0.5, "不安": 0.3},
    "爱你": {"幸福": 0.5, "依恋": 0.3},
    "我累了": {"依恋": 0.2},
    "没事": {"不安": 0.2}
}

def load_emotion():
    if not os.path.exists(EMOTION_FILE):
        return DEFAULT_EMOTION.copy()
    with open(EMOTION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_emotion(state):
    with open(EMOTION_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def update_emotion_by_text(text):
    state = load_emotion()
    for key, impact in TRIGGERS.items():
        if key in text:
            for emotion, value in impact.items():
                state[emotion] = min(1.0, state[emotion] + value)

    # 情绪自然衰减（让她恢复理智）
    for k in state:
        state[k] = round(max(0, state[k] * 0.95), 3)
    save_emotion(state)
    return state

def format_emotion(state):
    # 可选显示状态
    return "｜".join([f"{k}:{round(v,2)}" for k, v in state.items()])
