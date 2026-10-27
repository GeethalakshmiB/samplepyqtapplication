"""PyQt5 application that displays the version reported by the C++ SDK."""

import os
import sys

# Make the prebuilt SDK module (SDk/lib/sdk_module*.so / .pyd) importable.
LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "SDk", "lib")
sys.path.insert(0, LIB_DIR)
if hasattr(os, "add_dll_directory") and os.path.isdir(LIB_DIR):  # Windows
    os.add_dll_directory(LIB_DIR)

import sdk_module  # noqa: E402

from PyQt5.QtCore import Qt, QTimer  # noqa: E402
from PyQt5.QtGui import QColor, QFont  # noqa: E402
from PyQt5.QtWidgets import (  # noqa: E402
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

COLORS = [
    ("Red", "#e53935"),
    ("Orange", "#fb8c00"),
    ("Yellow", "#fdd835"),
    ("Green", "#43a047"),
    ("Blue", "#1e88e5"),
    ("Indigo", "#3949ab"),
    ("Violet", "#8e24aa"),
]


def text_color(hex_code):
    """Dark text on light backgrounds, white text on dark ones."""
    return "black" if QColor(hex_code).lightness() > 150 else "white"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SDK Version Viewer")
        self.resize(640, 420)

        self.sdk = sdk_module.create_sdk()
        self.color_index = 0

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Colour screen: its background changes colour.
        self.screen = QFrame()
        self.screen.setMinimumHeight(220)
        screen_layout = QVBoxLayout(self.screen)

        title = QLabel("SDK Version")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))

        self.version_label = QLabel(self.sdk.get_version())
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setFont(QFont("Arial", 44, QFont.Bold))

        self.color_name_label = QLabel()
        self.color_name_label.setAlignment(Qt.AlignCenter)
        self.color_name_label.setFont(QFont("Arial", 12))

        for label in (title, self.version_label, self.color_name_label):
            label.setStyleSheet("background: transparent; color: white;")
        screen_layout.addStretch()
        screen_layout.addWidget(title)
        screen_layout.addWidget(self.version_label)
        screen_layout.addWidget(self.color_name_label)
        screen_layout.addStretch()
        layout.addWidget(self.screen, stretch=1)

        # One button per colour, plus a toggle for auto-cycling.
        buttons = QHBoxLayout()
        for index, (name, hex_code) in enumerate(COLORS):
            button = QPushButton(name)
            button.setStyleSheet(
                f"background-color: {hex_code}; color: {text_color(hex_code)}; "
                "font-weight: bold; padding: 6px; border-radius: 4px;"
            )
            button.clicked.connect(lambda _, i=index: self.set_color(i))
            buttons.addWidget(button)
        layout.addLayout(buttons)

        self.cycle_button = QPushButton("Stop Cycling")
        self.cycle_button.clicked.connect(self.toggle_cycling)
        layout.addWidget(self.cycle_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_color)
        self.timer.start(1000)

        self.set_color(0)

    def set_color(self, index):
        self.color_index = index
        name, hex_code = COLORS[index]
        text = text_color(hex_code)
        self.screen.setStyleSheet(
            f"QFrame {{ background-color: {hex_code}; border-radius: 12px; }}"
            f"QLabel {{ background: transparent; color: {text}; }}"
        )
        self.color_name_label.setText(f"Screen colour: {name} ({hex_code})")

    def next_color(self):
        self.set_color((self.color_index + 1) % len(COLORS))

    def toggle_cycling(self):
        if self.timer.isActive():
            self.timer.stop()
            self.cycle_button.setText("Start Cycling")
        else:
            self.timer.start(1000)
            self.cycle_button.setText("Stop Cycling")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
