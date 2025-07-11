import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-8:], f, ensure_ascii=False, indent=2)  # 最多保存8条

def add_to_memory(role, content):
    memory = load_memory()
    memory.append({"role": role, "content": content})
    save_memory(memory)
