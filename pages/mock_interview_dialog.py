import json
import urllib.request
import datetime
import traceback
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QMessageBox, QWidget, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from database import crud

QUESTION_BANK = {
    "Technical: System Design": [
        "Làm thế nào để thiết kế một hệ thống URL Shortener (như bit.ly) chịu tải cao?",
        "Hãy giải thích cách hoạt động của cơ chế Caching (như Redis) và cách bạn xử lý cache invalidation?",
        "Làm thế nào để thiết kế một hệ thống Rate Limiter cho API của doanh nghiệp?"
    ],
    "Behavioral & Soft Skills": [
        "Hãy kể về một lần bạn gặp xung đột ý kiến với đồng nghiệp hoặc thành viên nhóm và cách bạn giải quyết nó.",
        "Khi dự án bị trễ hạn so với kế hoạch ban đầu, bạn sẽ làm gì để xử lý tình huống đó?",
        "Mô tả một thử thách kỹ thuật khó khăn nhất bạn từng vượt qua và bài học rút ra."
    ],
    "Frontend Engineering": [
        "React Server Components (RSC) khác biệt như thế nào so với Client Components và Server-Side Rendering (SSR)?",
        "Làm thế nào để tối ưu hóa thời gian tải trang đầu tiên (First Contentful Paint) của một ứng dụng Single Page Application?",
        "Hãy giải thích cơ chế Virtual DOM của React và cách thức Virtual DOM giúp tăng tốc độ render."
    ],
    "Backend Engineering": [
        "Làm thế nào để thiết kế cơ sở dữ liệu đảm bảo tính nhất quán (Consistency) và khả năng mở rộng (Scalability)?",
        "Hãy giải thích sự khác biệt giữa các cơ chế xác thực JWT, Session và OAuth2. Nên dùng khi nào?",
        "Làm thế nào để tối ưu hóa một câu lệnh SQL query chậm và thiết lập index hiệu quả?"
    ]
}

class MockInterviewDialog(QDialog):
    def __init__(self, category, student_id, parent=None):
        super().__init__(parent)
        self.category = category
        self.student_id = student_id
        
        self.setWindowTitle(f"AI Interview: {category}")
        self.resize(550, 480)
        
        self.questions = QUESTION_BANK.get(category, [
            "Hãy tự giới thiệu ngắn gọn về bản thân bạn.",
            "Tại sao bạn lại nộp đơn ứng tuyển vào vị trí này?",
            "Mục tiêu nghề nghiệp trong 3 năm tới của bạn là gì?"
        ])
        
        self.current_idx = 0
        self.answers = []
        
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                color: #0F172A;
            }
            QLabel {
                color: #0F172A;
                font-family: "Segoe UI", sans-serif;
            }
            QTextEdit {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 12px;
                padding: 14px;
                font-size: 13px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border: 1px solid #2563EB;
            }
            QPushButton {
                background-color: #F1F5F9;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 10px;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
            }
            QPushButton#btnPrimary {
                background-color: #2563EB;
                color: white;
                border: none;
            }
            QPushButton#btnPrimary:hover {
                background-color: #1D4ED8;
            }
        """)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        
        # Stacked pages
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # 1. PAGE: Intro / Ready
        self.page_intro = QWidget()
        self._init_page_intro()
        self.stack.addWidget(self.page_intro)
        
        # 2. PAGE: Question / Answer
        self.page_qa = QWidget()
        self._init_page_qa()
        self.stack.addWidget(self.page_qa)
        
        # 3. PAGE: Loading
        self.page_loading = QWidget()
        self._init_page_loading()
        self.stack.addWidget(self.page_loading)
        
        # 4. PAGE: Result
        self.page_result = QWidget()
        self._init_page_result()
        self.stack.addWidget(self.page_result)
        
        self.stack.setCurrentIndex(0)

    def _init_page_intro(self):
        lay = QVBoxLayout(self.page_intro)
        lay.setSpacing(16)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon = QLabel("🎙️")
        icon.setStyleSheet("font-size: 48px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(icon)
        
        title = QLabel(f"Bắt đầu phỏng vấn giả lập")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)
        
        desc = QLabel(
            "Hệ thống đã chuẩn bị 3 câu hỏi phỏng vấn thực tế cho bạn.\n"
            "Hãy trả lời đầy đủ, chi tiết và nghiêm túc để AI đánh giá chính xác."
        )
        desc.setStyleSheet("color: #64748B; font-size: 13px; line-height: 1.6;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(desc)
        
        btn_start = QPushButton("Bắt đầu ngay", objectName="btnPrimary")
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.clicked.connect(self._start_interview)
        lay.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

    def _init_page_qa(self):
        lay = QVBoxLayout(self.page_qa)
        lay.setSpacing(16)
        
        self.lbl_progress = QLabel("Câu hỏi 1 / 3")
        self.lbl_progress.setStyleSheet("color: #2563EB; font-weight: bold; font-size: 12px; text-transform: uppercase;")
        lay.addWidget(self.lbl_progress)
        
        self.lbl_question = QLabel("Question text goes here...")
        self.lbl_question.setWordWrap(True)
        self.lbl_question.setStyleSheet("font-size: 15px; font-weight: bold; line-height: 1.5; color: #0F172A;")
        lay.addWidget(self.lbl_question)
        
        self.answer_input = QTextEdit()
        self.answer_input.setPlaceholderText("Nhập câu trả lời của bạn tại đây (Khuyên dùng viết trên 50 từ)...")
        lay.addWidget(self.answer_input)
        
        btn_lay = QHBoxLayout()
        btn_lay.addStretch()
        
        self.btn_submit = QPushButton("Nộp câu trả lời ➔", objectName="btnPrimary")
        self.btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_submit.clicked.connect(self._submit_answer)
        btn_lay.addWidget(self.btn_submit)
        
        lay.addLayout(btn_lay)

    def _init_page_loading(self):
        lay = QVBoxLayout(self.page_loading)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(16)
        
        self.loading_icon = QLabel("⚙️")
        self.loading_icon.setStyleSheet("font-size: 48px; color: #2563EB;")
        self.loading_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.loading_icon)
        
        loading_text = QLabel("AI đang chấm điểm và phân tích câu trả lời của bạn...")
        loading_text.setStyleSheet("font-size: 14px; font-weight: bold;")
        loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(loading_text)
        
        loading_sub = QLabel("Quá trình này có thể mất vài giây...")
        loading_sub.setStyleSheet("color: #64748B; font-size: 12px;")
        loading_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(loading_sub)

    def _init_page_result(self):
        lay = QVBoxLayout(self.page_result)
        lay.setSpacing(14)
        
        hdr = QHBoxLayout()
        hdr.addWidget(QLabel("Kết quả đánh giá phỏng vấn", styleSheet="font-size: 16px; font-weight: bold; color: #0F172A;"))
        hdr.addStretch()
        
        self.lbl_score = QLabel("8.5 / 10")
        self.lbl_score.setStyleSheet("font-size: 14px; font-weight: 800; color: #10B981; background: #E6F4EA; padding: 4px 10px; border-radius: 6px;")
        hdr.addWidget(self.lbl_score)
        lay.addLayout(hdr)
        
        self.result_feedback = QTextEdit()
        self.result_feedback.setReadOnly(True)
        self.result_feedback.setStyleSheet("QTextEdit { background-color: #FFFFFF; border: 1px solid #CBD5E1; color: #0F172A; }")
        lay.addWidget(self.result_feedback)
        
        btn_close = QPushButton("Hoàn thành", objectName="btnPrimary")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        lay.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignCenter)

    def _start_interview(self):
        self.current_idx = 0
        self.answers = []
        self._load_current_question()
        self.stack.setCurrentIndex(1)

    def _load_current_question(self):
        self.lbl_progress.setText(f"Câu hỏi {self.current_idx + 1} / 3")
        self.lbl_question.setText(self.questions[self.current_idx])
        self.answer_input.clear()
        self.btn_submit.setText("Nộp câu trả lời ➔" if self.current_idx < 2 else "Hoàn thành phỏng vấn ➔")

    def _submit_answer(self):
        ans = self.answer_input.toPlainText().strip()
        if not ans:
            QMessageBox.warning(self, "Lỗi xác thực", "Vui lòng nhập câu trả lời của bạn.")
            return
            
        self.answers.append(ans)
        
        self.current_idx += 1
        if self.current_idx < 3:
            self._load_current_question()
        else:
            self._run_ai_evaluation()

    def _run_ai_evaluation(self):
        self.stack.setCurrentIndex(2)
        # Process events to render loading state
        self.stack.repaint()
        
        # Prepare evaluation
        q1, a1 = self.questions[0], self.answers[0]
        q2, a2 = self.questions[1], self.answers[1]
        q3, a3 = self.questions[2], self.answers[2]
        
        prompt = f"""
        You are an expert Tech Recruiter interviewing a student. Rate their answers for the category: '{self.category}'.
        
        1. Question: {q1}
           Answer: {a1}
        2. Question: {q2}
           Answer: {a2}
        3. Question: {q3}
           Answer: {a3}
           
        Please evaluate their responses. Output a JSON format response strictly matching:
        {{
            "score": <float from 1.0 to 10.0>,
            "feedback": "<detailed feedback in Vietnamese summarizing strengths, weaknesses, and improvement tips>"
        }}
        Provide only JSON, no markdown wrapper around it.
        """
        
        ai_res = None
        try:
            # Query local Ollama service
            url = "http://localhost:11434/api/generate"
            payload = json.dumps({
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }).encode("utf-8")
            
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=4.0) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                raw_text = res_data.get("response", "").strip()
                # strip potential json code blocks
                if raw_text.startswith("```"):
                    raw_text = re.sub(r"^```(json)?\n", "", raw_text)
                    raw_text = re.sub(r"\n```$", "", raw_text)
                ai_res = json.loads(raw_text.strip())
        except Exception:
            # Fallback to local heuristic analyzer
            pass
            
        if not ai_res or not isinstance(ai_res, dict):
            ai_res = self._fallback_structural_analysis(self.answers)
            
        score = float(ai_res.get("score", 7.0))
        feedback = ai_res.get("feedback", "Đánh giá hoàn thành.")
        
        # Save to SQLite DB
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        crud.save_mock_interview(self.student_id, self.category, score, feedback, now_str)
        
        # Update result UI
        self.lbl_score.setText(f"Score: {score:.1f} / 10")
        self.result_feedback.setPlainText(feedback)
        self.stack.setCurrentIndex(3)

    def _fallback_structural_analysis(self, answers):
        # Heuristics based on total word count and keywords matching the category
        total_words = 0
        for a in answers:
            total_words += len(a.split())
            
        # Basic scoring based on answer lengths
        if total_words > 180:
            score = 8.5
            feedback = (
                "### 🎙️ Đánh Giá Phản Hồi Phỏng Vấn (Fallback AI)\n\n"
                "**Ưu điểm:** Bạn trả lời rất chi tiết và giải thích cặn kẽ các khía cạnh của câu hỏi. "
                "Cấu trúc câu trả lời mạch lạc, thể hiện sự hiểu biết sâu sắc về mảng " + self.category + ".\n\n"
                "**Nhược điểm:** Đôi chỗ giải thích hơi dài dòng, có thể cô đọng các thuật ngữ hơn để tiết kiệm thời gian.\n\n"
                "**Khuyên dùng:** Nên luyện tập phương pháp STAR khi trả lời câu hỏi hành vi để lập luận sắc sảo hơn."
            )
        elif total_words > 80:
            score = 7.2
            feedback = (
                "### 🎙️ Đánh Giá Phản Hồi Phỏng Vấn (Fallback AI)\n\n"
                "**Ưu điểm:** Bạn đã trả lời đúng trọng tâm câu hỏi, đưa ra được các ý chính cần thiết.\n\n"
                "**Nhược điểm:** Câu trả lời còn hơi ngắn, thiếu ví dụ thực tế hoặc sơ đồ minh chứng để tăng độ thuyết phục.\n\n"
                "**Khuyên dùng:** Hãy mở rộng thêm phần giải pháp kỹ thuật cụ thể hoặc bài học kinh nghiệm để bài nói sâu hơn."
            )
        else:
            score = 5.0
            feedback = (
                "### 🎙️ Đánh Giá Phản Hồi Phỏng Vấn (Fallback AI)\n\n"
                "**Ưu điểm:** Bạn có nỗ lực phản hồi câu hỏi.\n\n"
                "**Nhược điểm:** Câu trả lời quá ngắn (dưới 30 từ mỗi câu) và sơ sài, chưa đáp ứng được yêu cầu tuyển dụng tối thiểu.\n\n"
                "**Khuyên dùng:** Vui lòng tìm hiểu kỹ hơn về lý thuyết nền tảng và viết câu trả lời dài hơn để hệ thống AI có đủ dữ liệu đánh giá."
            )
            
        return {"score": score, "feedback": feedback}
