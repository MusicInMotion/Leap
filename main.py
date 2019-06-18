from PyQt5 import QtWidgets
from SelectionMenu import SelectionMenu

def main():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    window.showFullScreen()

    layout = QtWidgets.QGridLayout(window)
    
    menu = SelectionMenu(layout)
    
    layout.addWidget(QtWidgets.QLabel(), 0, 0)
    layout.addWidget(menu, 1, 0)
    layout.addWidget(QtWidgets.QLabel(), 2, 0)
 
    app.exec_()
    del app

if __name__ == "__main__":
    main()