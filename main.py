"""
===============================================================================
AI CAREER BRIDGE
===============================================================================

Hey team! This is the main file that launches our app window.
chung may. lan sau chay code thi chay trong nay. con may cai khac chay cho khac

How the AI Brain Works for this Project:
ta chay gemma 4 26B A4B tren may macbook cua ta

- MODE 1 (Remote Testing): When you are testing this at home, the app will
  talk to a Cloudflare link that secretly connects to the MacBook over the internet.
- MODE 2 (Campus Mode): When we are at university, the app will just look locally
  on the MacBook to save battery and skip the Wi-Fi lag.

  noi chung thi, khi o nha test thi chinh key API lai, len truong test thi khac.
  thi o nha thi luc do ta gui cho cai API key, chung may xem huong han ben duoi la duoc.


===============================================================================
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class CareerBridgeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Setup the main window
        self.setWindowTitle("AI Career Bridge")
        self.setGeometry(100, 100, 600, 400)

        # 2. Put some basic text on the screen
        layout = QVBoxLayout()
        self.status_label = QLabel("Welcome to the Bridge. Waiting for AI connection...")
        layout.addWidget(self.status_label)

        # 3. Apply the layout to the window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ---------------------------------------------------------------------
        # AI CONNECTION SETUP (COMING SOON)
        # ---------------------------------------------------------------------
        # TODO: We will add the Ollama API connection here later.
        # Example: api_link = "https://[our-cloudflare-link].trycloudflare.com"
        #
        # NOTE FOR LATER: When we send a resume to the AI, we can't do it on the
        # main screen, or the app will freeze while the Mac thinks. We will need
        # to run it in the background.
        # ---------------------------------------------------------------------


if __name__ == "__main__":
    # Start the app
    app = QApplication(sys.argv)
    window = CareerBridgeWindow()
    window.show()
    sys.exit(app.exec())