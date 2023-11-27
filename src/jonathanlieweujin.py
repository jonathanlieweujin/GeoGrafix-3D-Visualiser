import sys
from PyQt5 import QtWidgets

from gui_window import GuiWindow

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    m_window = QtWidgets.QMainWindow()
    ui = GuiWindow(m_window)
    m_window.show()
    sys.exit(app.exec_())

# pyinstaller --onefile -w --icon=./images/icon.ico jonathanlieweujin.py
