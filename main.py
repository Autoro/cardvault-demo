import sys
import card_vault
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

def main():
    app = QGuiApplication(sys.argv)
    QQuickStyle.setStyle("Material")

    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.loadFromModule("app", "main")

    if not engine.rootObjects():
        sys.exit(-1)
    
    exit_code = app.exec()
    del engine
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()