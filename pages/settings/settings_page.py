from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                             QStackedWidget, QLabel, QPushButton)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QCursor

from .settings_sidebar import SettingsSidebar
from .profile_identity_workspace import ProfileIdentityWorkspace
from .preferences_workspace import PreferencesWorkspace
from .notifications_workspace import NotificationsIntelligenceCenter
from .appearance_workspace import AppearanceWorkspace
from .accessibility_workspace import AccessibilityWorkspace
from .privacy_security_workspace import PrivacySecurityWorkspace
from .ai_personalization_workspace import AIPersonalityWorkspace
from .integrations_marketplace_hub import IntegrationsMarketplaceHub
from .about_workspace import AboutApplicationWorkspace

from .branding_insights_panel import BrandingInsightsPanel
from .ai_workflow_panel import AIWorkflowPanel
from .ai_notification_panel import AINotificationPanel
from .ai_visual_panel import AIVisualPanel
from .ai_accessibility_panel import AIAccessibilityPanel
from .ai_security_panel import AISecurityPanel
from .ai_personalization_panel import AIPersonalizationPanel
from .ai_integration_panel import AIIntegrationPanel
from .ai_system_panel import AISystemPanel

from components import CollapsiblePanel

class ToggleSwitch(QWidget):
    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self._checked = checked
        self._thumb_pos = 22 if checked else 2
        
        self.animation = QPropertyAnimation(self, b"thumb_pos")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setDuration(200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    @pyqtProperty(int)
    def thumb_pos(self):
        return self._thumb_pos
        
    @thumb_pos.setter
    def thumb_pos(self, pos):
        self._thumb_pos = pos
        self.update()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            self.animation.setStartValue(self._thumb_pos)
            self.animation.setEndValue(22 if self._checked else 2)
            self.animation.start()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bg_color = QColor("#38BDF8") if self._checked else QColor("#E2E8F0")
        painter.setBrush(QBrush(bg_color)); painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        painter.setBrush(QBrush(QColor("#FFFFFF"))); painter.drawEllipse(self._thumb_pos, 2, 20, 20)

class SettingsPage(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName("SettingsPage")
        self.setStyleSheet("background-color: #F8FAFC;")
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Left Sidebar
        self.sidebar_content = SettingsSidebar()
        self.sidebar_content.navigation_requested.connect(self._handle_navigation)
        self.left_panel = CollapsiblePanel(self.sidebar_content, orientation="left")
        self.main_layout.addWidget(self.left_panel)

        # 2. Main Stacked Workspace
        self.workspace_container = QWidget()
        self.workspace_layout = QVBoxLayout(self.workspace_container)
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.setSpacing(0)

        self._setup_top_header()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(ProfileIdentityWorkspace())       # 0
        self.stacked_widget.addWidget(PreferencesWorkspace())           # 1
        self.stacked_widget.addWidget(NotificationsIntelligenceCenter()) # 2
        self.stacked_widget.addWidget(AppearanceWorkspace())            # 3
        self.stacked_widget.addWidget(AccessibilityWorkspace())         # 4
        self.stacked_widget.addWidget(PrivacySecurityWorkspace())       # 5
        self.stacked_widget.addWidget(AIPersonalityWorkspace())         # 6
        self.stacked_widget.addWidget(IntegrationsMarketplaceHub())      # 7
        self.stacked_widget.addWidget(AboutApplicationWorkspace())       # 8
        
        # Placeholders
        for i in range(1):
            placeholder = QWidget()
            pl = QVBoxLayout(placeholder); pl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl = QLabel(f"Section {i+10} Coming Soon")
            lbl.setStyleSheet("font-size: 16px; color: #94A3B8; font-weight: 600;")
            pl.addWidget(lbl); self.stacked_widget.addWidget(placeholder)

        self.workspace_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.workspace_container, 1)

        # 3. Right Intelligence Stack
        self.right_stack = QStackedWidget()
        self.right_stack.addWidget(BrandingInsightsPanel()) # 0
        self.right_stack.addWidget(AIWorkflowPanel())       # 1
        self.right_stack.addWidget(AINotificationPanel())  # 2
        self.right_stack.addWidget(AIVisualPanel())        # 3
        self.right_stack.addWidget(AIAccessibilityPanel()) # 4
        self.right_stack.addWidget(AISecurityPanel())      # 5
        self.right_stack.addWidget(AIPersonalizationPanel()) # 6
        self.right_stack.addWidget(AIIntegrationPanel())   # 7
        self.right_stack.addWidget(AISystemPanel())        # 8
        
        # Add placeholders for other right panels
        for _ in range(1):
            w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(24,24,24,24)
            l.addWidget(QLabel("Insights Coming Soon", styleSheet="color: #94A3B8; font-size: 12px; font-weight: 800;"))
            l.addStretch(); self.right_stack.addWidget(w)

        self.right_panel = CollapsiblePanel(self.right_stack, orientation="right")
        self.main_layout.addWidget(self.right_panel)

    def _setup_top_header(self):
        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        hl = QHBoxLayout(header); hl.setContentsMargins(32, 0, 32, 0); hl.setSpacing(24)
        title_v = QVBoxLayout(); title_v.setSpacing(2); title_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.tab_title_lbl = QLabel("Profile & Identity")
        self.tab_title_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A; border: none;")
        self.summary_lbl = QLabel("Manage your professional presence and personal branding")
        self.summary_lbl.setStyleSheet("font-size: 12px; color: #64748B; border: none;")
        title_v.addWidget(self.tab_title_lbl); title_v.addWidget(self.summary_lbl); hl.addLayout(title_v); hl.addStretch()
        btn_save = QPushButton("Save Changes")
        btn_save.setStyleSheet("background: #0F172A; color: white; border-radius: 10px; font-weight: 700; font-size: 12px; height: 36px; padding: 0 16px;")
        hl.addWidget(btn_save); self.workspace_layout.addWidget(header)

    def _handle_navigation(self, idx):
        self.stacked_widget.setCurrentIndex(idx)
        self.right_stack.setCurrentIndex(idx)
        titles = [
            "Profile & Identity", "Preferences", "Notifications", "Appearance", 
            "Accessibility", "Privacy & Security", "AI Personalization", 
            "Integrations Hub", "About Application"
        ]
        summaries = [
            "Manage your professional presence and personal branding",
            "Customize workspace behavior and interaction patterns",
            "Configure how you receive updates and alerts",
            "Personalize themes, colors, and visual styles",
            "Optimize the workspace for inclusive experience",
            "Control your trust and account protection",
            "Configure AI behaviors and predictive assistance",
            "Connect third-party services and manage API workflows",
            "Application version and system intelligence"
        ]
        self.tab_title_lbl.setText(titles[idx])
        self.summary_lbl.setText(summaries[idx])
