import requests
import time
import tkinter as tk
from tkinter import ttk, scrolledtext
from NovaForger import ChatModel

class BilibiliChatHistory:
    def __init__(self, room_id, BASEURL, modelname, apikey):
        self.base_url = "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory"
        self.room_id = room_id
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Origin": "https://www.bilibili.com"
        }
        self.seen_messages = set()

        # Define AI model parameters
        self.BASEURL = BASEURL
        self.modelname = modelname
        self.apikey = apikey
        self.systemprompt = """You are an assistant helping a Japanese streamer understand Chinese viewers. Your input is chat messages (danmu) sent by Chinese viewers. Your tasks are:
        
        1. Accurately translate the danmu into Japanese, including internet slang and colloquialisms.
        2. Provide appropriate response suggestions for the streamer, considering the following:
           - Friendly and positive tone
           - Moderate length (15-30 Japanese characters)
           - Consider cultural differences between China and Japan to avoid misunderstandings
           - For inappropriate or controversial content, provide tactful response suggestions
        
        Output format:
        Translation: "Japanese translation"
        Recommended response: "Suggested response in Japanese"
        
        Example:
        Input: "你好啊"
        Output:
        翻訳:「こんにちは」
        おすすめの返事の言葉:「こんにちは！みなさん、元気ですか？一緒に楽しい配信にしましょうね！」
        
        If the danmu contains complex or culturally specific content, please provide a brief explanation.
        
        Note: Always maintain a respectful and positive atmosphere, and help the streamer navigate any cultural nuances or sensitivities.
        """
        self.history = [
            {"role": "system", "content": self.systemprompt},
        ]
        self.model = ChatModel(BASEURL=self.BASEURL, modelname=self.modelname, apikey=self.apikey)

    def fetch_chat_history(self):
        params = {"roomid": self.room_id}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    @staticmethod
    def parse_chat_data(chat_data_dict):
        # 直接使用传入的字典
        chat_data = chat_data_dict
        
        # 检查是否存在'data'键和'room'列表
        if 'data' in chat_data and 'room' in chat_data['data']:
            room_messages = chat_data['data']['room']
            parsed_messages = []
            
            # 遍历消息列表
            for message in room_messages:
                # 提取消息文本、用户昵称、用户头像URL和时间戳
                text = message.get('text', 'No text available')
                nickname = message.get('nickname', 'No nickname available')
                timeline = message.get('timeline', 'No timeline available')
                message_id = message.get('id_str', 'No id available')
                
                # 创建一个包含所需信息的消息字典
                parsed_message = {
                    'text': text,
                    'nickname': nickname,
                    'timeline': timeline,
                    'id': message_id
                }
                
                # 将解析后的消息添加到列表中
                parsed_messages.append(parsed_message)
            
            return parsed_messages
        else:
            return "Invalid chat data format."

    def fetch_and_parse(self):
        chat_data = self.fetch_chat_history()
        if chat_data:
            parsed_chat = self.parse_chat_data(chat_data)
            new_messages = []
            
            for message in parsed_chat:
                if message['id'] not in self.seen_messages:
                    self.seen_messages.add(message['id'])
                    
                    # 使用AI模型处理消息
                    ai_response = self.model.run(content=message['text'], history=self.history)
                    message['AIMessage'] = ai_response
                    
                    new_messages.append(message)
            
            return new_messages
        return []

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("哔哩哔哩チャット履歴")
        self.geometry("700x500")
        
        # ラベルと入力フィールド
        tk.Label(self, text="モデルURL:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.url_entry = tk.Entry(self)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(self, text="モデル名:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.model_entry = tk.Entry(self)
        self.model_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(self, text="APIキー:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.apikey_entry = tk.Entry(self)
        self.apikey_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(self, text="ルームID:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.roomid_entry = tk.Entry(self)
        self.roomid_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # 実行ボタン
        self.run_button = tk.Button(self, text="開始", command=self.run_chat_history)
        self.run_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # チャット履歴表示エリア
        self.chat_display = scrolledtext.ScrolledText(self, width=80, height=20)
        self.chat_display.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def run_chat_history(self):
        BASEURL = self.url_entry.get()
        modelname = self.model_entry.get()
        apikey = self.apikey_entry.get()
        room_id = self.roomid_entry.get()
        
        self.bilibili_chat = BilibiliChatHistory(room_id, BASEURL, modelname, apikey)
        self.update_chat_history()

    def update_chat_history(self):
        new_messages = self.bilibili_chat.fetch_and_parse()
        if new_messages:
            for message in new_messages:
                display_message = f"ユーザー: {message['nickname']}\n時刻: {message['timeline']}\nチャット: {message['text']}\nAI翻訳: {message['AIMessage']}\n\n"
                self.chat_display.insert(tk.END, display_message)
        self.after(2000, self.update_chat_history)

if __name__ == "__main__":
    app = Application()
    app.mainloop()