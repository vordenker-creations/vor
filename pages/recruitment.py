import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame, QGridLayout,
                             QLineEdit, QProgressBar, QGraphicsDropShadowEffect,
                             QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QRectF, QPointF, QSize
from PyQt6.QtGui import (QColor, QPainter, QPen, QBrush, QFont, QPolygonF, 
                         QLinearGradient, QPainterPath)
import math

# Design Constants
BG_COLOR = "#F8FAFC"
CARD_BG = "#FFFFFF"
BORDER_COLOR = "#E2E8F0"
TEXT_PRIMARY = "#0F172A"
TEXT_SECONDARY = "#64748B"

ACCENT_PRIMARY = "#38BDF8"
ACCENT_SECONDARY = "#2DD4BF"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"

class ShadowCard(QFrame):
    def __init__(self, radius=20, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: {radius}px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)
        self.internal_layout = QVBoxLayout(self)
        self.internal_layout.setContentsMargins(20, 20, 20, 20)
        self.internal_layout.setSpacing(10)

class RadarChartMock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 240)
        self.skills = ["Python", "PyTorch", "System Design", "Cloud", "Mathematics", "DevOps"]
        self.current = [0.8, 0.7, 0.5, 0.4, 0.9, 0.3]
        self.target = [0.95, 0.9, 0.8, 0.7, 0.95, 0.6]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 40
        num_points = len(self.skills)
        angle_step = 2 * math.pi / num_points

        # Draw grid
        painter.setPen(QPen(QColor(BORDER_COLOR), 1, Qt.PenStyle.DashLine))
        for i in range(1, 5):
            r = radius * (i / 4)
            path = QPainterPath()
            for j in range(num_points):
                angle = j * angle_step - math.pi / 2
                p = center + QPointF(r * math.cos(angle), r * math.sin(angle))
                if j == 0: path.moveTo(p)
                else: path.lineTo(p)
            path.closeSubpath()
            painter.drawPath(path)

        for i in range(num_points):
            angle = i * angle_step - math.pi / 2
            p = center + QPointF(radius * math.cos(angle), radius * math.sin(angle))
            painter.drawLine(center, p)
            
            # Draw Labels
            text_p = center + QPointF((radius + 20) * math.cos(angle), (radius + 20) * math.sin(angle))
            painter.setPen(QPen(QColor(TEXT_SECONDARY)))
            painter.setFont(QFont("Inter", 8))
            painter.drawText(QRectF(text_p.x()-40, text_p.y()-10, 80, 20), Qt.AlignmentFlag.AlignCenter, self.skills[i])

        # Draw Target Area
        self._draw_poly(painter, center, radius, self.target, QColor(ACCENT_PRIMARY), 0.1)
        # Draw Current Area
        self._draw_poly(painter, center, radius, self.current, QColor(ACCENT_SECONDARY), 0.5)

    def _draw_poly(self, painter, center, radius, values, color, alpha):
        angle_step = 2 * math.pi / len(values)
        poly = QPolygonF()
        for i, val in enumerate(values):
            angle = i * angle_step - math.pi / 2
            r = radius * val
            poly.append(center + QPointF(r * math.cos(angle), r * math.sin(angle)))
        
        fill_color = QColor(color)
        fill_color.setAlphaF(alpha)
        painter.setBrush(QBrush(fill_color))
        painter.setPen(QPen(color, 2))
        painter.drawPolygon(poly)

class LineChartMock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.data = [20, 35, 25, 45, 60, 55, 80]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if not self.data: return
        
        w = self.width()
        h = self.height()
        max_val = max(self.data)
        x_step = w / (len(self.data) - 1)
        
        path = QPainterPath()
        for i, val in enumerate(self.data):
            x = i * x_step
            y = h - (val / max_val * h * 0.8) - 10
            if i == 0: path.moveTo(x, y)
            else: path.lineTo(x, y)
            
        painter.setPen(QPen(QColor(ACCENT_PRIMARY), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPath(path)
        
        # Area fill
        fill_path = QPainterPath(path)
        fill_path.lineTo(w, h)
        fill_path.lineTo(0, h)
        fill_path.closeSubpath()
        
        grad = QLinearGradient(0, 0, 0, h)
        c = QColor(ACCENT_PRIMARY)
        c.setAlphaF(0.2)
        grad.setColorAt(0, c)
        grad.setColorAt(1, Qt.GlobalColor.transparent)
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(fill_path)

class KPICard(ShadowCard):
    def __init__(self, title, value, subtext, color=ACCENT_PRIMARY):
        super().__init__(radius=16)
        l = self.internal_layout
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px; font-weight: 600; text-transform: uppercase;")
        l.addWidget(lbl_title)
        
        val_row = QHBoxLayout()
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 24px; font-weight: 700;")
        val_row.addWidget(lbl_val)
        
        mini_chart = LineChartMock()
        mini_chart.setFixedWidth(60)
        mini_chart.setFixedHeight(30)
        val_row.addWidget(mini_chart)
        l.addLayout(val_row)
        
        lbl_sub = QLabel(subtext)
        lbl_sub.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 500;")
        l.addWidget(lbl_sub)

class RecruitmentPage(QWidget):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("RecruitmentPage")
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 1. Top Toolbar
        self._setup_header()
        
        # Scroll Area for Content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(24)
        
        # 2. Main Analytics Workspace (Left)
        left_workspace = QVBoxLayout()
        left_workspace.setSpacing(24)
        
        # Section 1: Analytics Overview
        kpi_row = QHBoxLayout()
        kpi_row.addWidget(KPICard("Career Readiness", "84%", "↑ 12% from last month", COLOR_SUCCESS))
        kpi_row.addWidget(KPICard("Skill Completion", "18/24", "2 new skills earned", ACCENT_PRIMARY))
        kpi_row.addWidget(KPICard("Industry Match", "92%", "Top 5% of candidates", ACCENT_SECONDARY))
        kpi_row.addWidget(KPICard("Certifications", "4", "1 pending review", COLOR_WARNING))
        left_workspace.addLayout(kpi_row)
        
        # Section 2: Skill Gap Analysis
        skill_gap_row = QHBoxLayout()
        
        radar_card = ShadowCard()
        lbl_radar = QLabel("Technical Skill Alignment")
        lbl_radar.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        radar_card.internal_layout.addWidget(lbl_radar)
        radar_card.internal_layout.addWidget(RadarChartMock())
        skill_gap_row.addWidget(radar_card, 2)
        
        missing_skills_card = ShadowCard()
        ms_l = missing_skills_card.internal_layout
        lbl_ms = QLabel("Priority Missing Skills")
        lbl_ms.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        ms_l.addWidget(lbl_ms)
        
        for skill, diff, priority in [("Advanced Distributed Systems", "Hard", "High"), ("Kubernetes Security", "Medium", "Medium"), ("MLOps Pipelines", "Hard", "High")]:
            skill_item = QFrame()
            skill_item.setStyleSheet(f"background: #F1F5F9; border-radius: 10px; border: none;")
            sil = QHBoxLayout(skill_item)
            lbl_skill_name = QLabel(skill)
            lbl_skill_name.setStyleSheet(f"color: {TEXT_PRIMARY}; font-weight: 500;")
            sil.addWidget(lbl_skill_name)
            p_color = COLOR_DANGER if priority == "High" else COLOR_WARNING
            p_label = QLabel(priority)
            p_label.setStyleSheet(f"background: {p_color}22; color: {p_color}; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;")
            sil.addWidget(p_label)
            ms_l.addWidget(skill_item)
        ms_l.addStretch()
        skill_gap_row.addWidget(missing_skills_card, 1)
        left_workspace.addLayout(skill_gap_row)
        
        # Section 3: Career Readiness Panel
        readiness_row = QHBoxLayout()
        
        prob_card = ShadowCard()
        pl = prob_card.internal_layout
        lbl_prob = QLabel("Career Probability")
        lbl_prob.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        pl.addWidget(lbl_prob)
        for role, val in [("AI Engineer", 92), ("Data Scientist", 78), ("Backend Architect", 65)]:
            row = QVBoxLayout()
            rl = QHBoxLayout()
            lbl_role = QLabel(role)
            lbl_role.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px;")
            rl.addWidget(lbl_role)
            rl.addStretch()
            lbl_percent = QLabel(f"{val}%")
            lbl_percent.setStyleSheet(f"color: {TEXT_PRIMARY}; font-weight: 700;")
            rl.addWidget(lbl_percent)
            row.addLayout(rl)
            bar = QProgressBar()
            bar.setValue(val)
            bar.setFixedHeight(6)
            bar.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border-radius: 3px; }} QProgressBar::chunk {{ background: {ACCENT_PRIMARY}; border-radius: 3px; }}")
            row.addWidget(bar)
            pl.addLayout(row)
        readiness_row.addWidget(prob_card, 1)
        
        insights_card = ShadowCard()
        il = insights_card.internal_layout
        lbl_ai_ins = QLabel("AI Career Insights")
        lbl_ai_ins.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        il.addWidget(lbl_ai_ins)
        insight_box = QFrame()
        insight_box.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {ACCENT_PRIMARY}11, stop:1 {ACCENT_SECONDARY}11); border-radius: 12px; border: 1px solid {ACCENT_PRIMARY}33;")
        ibl = QVBoxLayout(insight_box)
        lbl_insight_text = QLabel("You're tracking well for 'Lead AI Engineer'. Strengthening your 'Distributed Systems' knowledge will increase your marketability by 15% in top-tier tech firms.")
        lbl_insight_text.setWordWrap(True)
        lbl_insight_text.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 13px; font-style: italic;")
        ibl.addWidget(lbl_insight_text)
        il.addWidget(insight_box)
        readiness_row.addWidget(insights_card, 1)
        left_workspace.addLayout(readiness_row)
        
        # Section 4: Certification Tracker
        lbl_cert_track = QLabel("Certification Tracker")
        lbl_cert_track.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 18px; font-weight: 700; margin-top: 8px;")
        left_workspace.addWidget(lbl_cert_track)
        cert_row = QHBoxLayout()
        for cert, prov, prog in [("AWS ML Specialty", "Amazon", 65), ("Google Cloud Architect", "Google", 40), ("Deep Learning Spec", "Coursera", 90)]:
            c_card = ShadowCard(radius=12)
            cl = c_card.internal_layout
            lbl_c_name = QLabel(cert)
            lbl_c_name.setStyleSheet(f"color: {TEXT_PRIMARY}; font-weight: 700; font-size: 14px;")
            cl.addWidget(lbl_c_name)
            lbl_c_prov = QLabel(prov)
            lbl_c_prov.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")
            cl.addWidget(lbl_c_prov)
            pb = QProgressBar()
            pb.setValue(prog)
            pb.setFixedHeight(4)
            pb.setStyleSheet(f"QProgressBar {{ background: #F1F5F9; border-radius: 2px; }} QProgressBar::chunk {{ background: {COLOR_SUCCESS}; border-radius: 2px; }}")
            cl.addWidget(pb)
            lbl_c_est = QLabel(f"Est. 2 weeks")
            lbl_c_est.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px;")
            cl.addWidget(lbl_c_est)
            cert_row.addWidget(c_card)
        left_workspace.addLayout(cert_row)
        
        # Section 5: Market Insights
        market_row = QHBoxLayout()
        trending_card = ShadowCard()
        tl = trending_card.internal_layout
        lbl_trend = QLabel("Trending Technologies")
        lbl_trend.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        tl.addWidget(lbl_trend)
        for tech, trend in [("LLMOps", "↑ 240%"), ("Rust", "↑ 85%"), ("Vector DBs", "↑ 150%")]:
            item = QHBoxLayout()
            lbl_tech = QLabel(tech)
            lbl_tech.setStyleSheet(f"color: {TEXT_PRIMARY}; font-weight: 500;")
            item.addWidget(lbl_tech)
            item.addStretch()
            lbl_trend_val = QLabel(trend)
            lbl_trend_val.setStyleSheet(f"color: {COLOR_SUCCESS}; font-weight: 700;")
            item.addWidget(lbl_trend_val)
            tl.addLayout(item)
        market_row.addWidget(trending_card, 1)
        
        market_graph_card = ShadowCard()
        mgl = market_graph_card.internal_layout
        lbl_m_graph = QLabel("Job Market Analytics (AI Roles)")
        lbl_m_graph.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        mgl.addWidget(lbl_m_graph)
        mgl.addWidget(LineChartMock())
        market_row.addWidget(market_graph_card, 2)
        left_workspace.addLayout(market_row)
        
        container_layout.addLayout(left_workspace, 1)
        
        # 3. Right AI Insights Panel
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(0, 0, 0, 0)
        right_panel.setSpacing(24)
        
        right_container = QWidget()
        right_container.setFixedWidth(320)
        right_container.setLayout(right_panel)
        
        # AI Suggestions
        ai_sugg = ShadowCard()
        asl = ai_sugg.internal_layout
        lbl_ai_sugg = QLabel("🎯 AI Suggestions")
        lbl_ai_sugg.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        asl.addWidget(lbl_ai_sugg)
        lbl_ai_sub = QLabel("Immediate Learning Priorities:")
        lbl_ai_sub.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px;")
        asl.addWidget(lbl_ai_sub)
        for sugg in ["Review Kafka partitioning", "Complete Docker Compose lab", "Finish PyTorch Lightning module"]:
            s_lbl = QLabel(f"• {sugg}")
            s_lbl.setWordWrap(True)
            s_lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 13px; margin-top: 4px;")
            asl.addWidget(s_lbl)
        right_panel.addWidget(ai_sugg)
        
        # Recent Achievements
        achieve = ShadowCard()
        acl = achieve.internal_layout
        lbl_ach = QLabel("🏆 Achievements")
        lbl_ach.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        acl.addWidget(lbl_ach)
        for a in ["Python Expert Badge", "SQL Optimization Master", "10 Day Streak"]:
            a_lbl = QLabel(f"✔ {a}")
            a_lbl.setStyleSheet(f"color: {COLOR_SUCCESS}; font-size: 13px; font-weight: 500; margin-top: 4px;")
            acl.addWidget(a_lbl)
        right_panel.addWidget(achieve)
        
        # Upcoming Goals
        goals = ShadowCard()
        gl = goals.internal_layout
        lbl_goals = QLabel("📅 Upcoming Goals")
        lbl_goals.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 700;")
        gl.addWidget(lbl_goals)
        for g, d in [("System Design Mock", "Tomorrow"), ("Cloud Practitioner Exam", "Friday"), ("Open Source Contrib", "Next Week")]:
            gr = QHBoxLayout()
            lbl_g_item = QLabel(g)
            lbl_g_item.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 13px;")
            gr.addWidget(lbl_g_item)
            gr.addStretch()
            lbl_g_date = QLabel(d)
            lbl_g_date.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px;")
            gr.addWidget(lbl_g_date)
            gl.addLayout(gr)
        right_panel.addWidget(goals)
        right_panel.addStretch()
        
        container_layout.addWidget(right_container)
        
        scroll.setWidget(container)
        self.main_layout.addWidget(scroll)

    def _setup_header(self):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(f"background-color: {CARD_BG}; border-bottom: 1px solid {BORDER_COLOR};")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(24, 0, 24, 0)
        
        # Breadcrumbs
        bc = QLabel("Career Analytics / <font color='#38BDF8'>AI Engineer</font>")
        bc.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; font-weight: 500;")
        hl.addWidget(bc)
        
        hl.addStretch()
        
        # Search Bar
        search = QLineEdit()
        search.setPlaceholderText("Search insights... (Ctrl+K)")
        search.setFixedWidth(300)
        search.setStyleSheet(f"""
            QLineEdit {{
                background-color: #F1F5F9;
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
                padding: 8px 12px;
                color: {TEXT_PRIMARY};
                font-size: 13px;
            }}
        """)
        hl.addWidget(search)
        
        # Action Buttons
        btn_ai = QPushButton("Generate AI Analysis")
        btn_ai.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_PRIMARY};
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
                border: none;
            }}
            QPushButton:hover {{ background-color: #0EA5E9; }}
        """)
        hl.addWidget(btn_ai)
        
        btn_exp = QPushButton("Export Report")
        btn_exp.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {TEXT_PRIMARY};
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: #F1F5F9; }}
        """)
        hl.addWidget(btn_exp)
        
        # Avatar Mock
        avatar = QLabel("JD")
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"""
            background-color: {ACCENT_SECONDARY};
            color: white;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
        """)
        hl.addWidget(avatar)
        
        self.main_layout.addWidget(header)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = RecruitmentPage()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())
