import customtkinter as ctk
import tkinter as tk
from config import *
from components import SaaSCard

class AIMentorUI(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(35, 20))
        ctk.CTkLabel(header, text="AI Mentor Chat", font=ctk.CTkFont(family=FONT_MAIN, size=24, weight="bold"), text_color=COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(header, text="🟢 Online", font=ctk.CTkFont(family=FONT_MAIN, size=12, weight="bold"), text_color=COLOR_SUCCESS).pack(side="left", padx=15)

        # Main Chat Area
        self.chat_card = SaaSCard(self)
        self.chat_card.pack(fill="both", expand=True, padx=25, pady=(0, 10))
        
        self.chat_box = ctk.CTkTextbox(self.chat_card, fg_color="transparent", text_color=COLOR_TEXT_MAIN, font=ctk.CTkFont(family=FONT_MAIN, size=14), wrap="word")
        self.chat_box.pack(fill="both", expand=True, padx=20, pady=20)
        self.chat_box.configure(state="disabled")

        # Action Chips Area
        self.chips_frame = ctk.CTkFrame(self.chat_card, fg_color="transparent")
        self.chips_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        chips = ["Phân tích CV", "Gợi ý Roadmap", "Luyện Phỏng vấn", "Giải thích Code"]
        for chip in chips:
            btn = ctk.CTkButton(self.chips_frame, text=chip, fg_color=COLOR_BG_APP, text_color=COLOR_PRIMARY, 
                                hover_color=COLOR_PRIMARY_LIGHT, font=ctk.CTkFont(size=12, weight="bold"), corner_radius=16, height=32,
                                command=lambda c=chip: self.send_message(c))
            btn.pack(side="left", padx=5)

        # Input Area
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=25, pady=(0, 30))
        
        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Hỏi AI Mentor bất cứ điều gì...", font=ctk.CTkFont(size=14), height=45, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.send_message())
        
        send_btn = ctk.CTkButton(input_frame, text="Gửi ➔", font=ctk.CTkFont(size=14, weight="bold"), fg_color=COLOR_PRIMARY, width=80, height=45, corner_radius=8, command=self.send_message)
        send_btn.pack(side="right")

        # Initial Greeting
        self.append_message("AI Mentor", "Chào bạn, tôi là AI Mentor. Hãy chọn một tùy chọn bên dưới hoặc đặt câu hỏi để tôi hỗ trợ bạn nhé!\n\nTôi có thể giúp bạn:\n- **Phân tích CV** và gợi ý cải thiện\n- Xây dựng **Roadmap** học tập cá nhân hóa\n- Giải thích các đoạn `code` phức tạp")

    def append_message(self, sender, text):
        self.chat_box.configure(state="normal")
        
        # Simple Markdown parsing (bold and inline code)
        self.chat_box.insert("end", f"\n{sender}:\n", "sender")
        
        # We can implement tag configs for bold and code
        self.chat_box.tag_config("sender", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"), foreground=get_color(COLOR_PRIMARY))
        self.chat_box.tag_config("bold", font=ctk.CTkFont(family=FONT_MAIN, size=14, weight="bold"))
        self.chat_box.tag_config("code", font=ctk.CTkFont(family="Consolas", size=13), background=get_color(COLOR_BG_APP), foreground=get_color(COLOR_WARNING))
        
        parts = text.split("**")
        for i, p in enumerate(parts):
            if i % 2 != 0:
                self.chat_box.insert("end", p, "bold")
            else:
                sub_parts = p.split("`")
                for j, sp in enumerate(sub_parts):
                    if j % 2 != 0:
                        self.chat_box.insert("end", sp, "code")
                    else:
                        self.chat_box.insert("end", sp)
        
        self.chat_box.insert("end", "\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.yview("end")

    def send_message(self, text=None):
        msg = text if text else self.entry.get()
        if not msg.strip(): return
        
        if not text:
            self.entry.delete(0, "end")
            
        self.append_message("Bạn", msg)
        
        # Mock AI Response
        self.after(500, lambda: self.append_message("AI Mentor", f"Tôi đang xử lý yêu cầu: **{msg}**. Bạn đợi một lát nhé. Dưới đây là ví dụ `print('Hello World')`."))

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    app.configure(fg_color=COLOR_BG_APP)
    page = AIMentorUI(app)
    page.pack(fill="both", expand=True)
    app.mainloop()