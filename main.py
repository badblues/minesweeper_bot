import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette, QPainter, QPen, QBrush, QColor
from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QStyleOption

class Cell(QtWidgets.QWidget):
    SIZE = 10

    def __init__ (self):
        super().__init__()
        self.setGeometry(0, 0, self.SIZE, self.SIZE)
        self.setFixedSize(QSize(self.SIZE, self.SIZE))
        self.setStyleSheet("QWidget {color: cyan}")
        self.repaint()

    def mousePressEvent(self, event):
        print("event:" + str(event.x()) + " " + str(event.y()))

    def paintEvent(self, e):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        painter.end()
        self.style().drawPrimitive()
       



class Field(QtWidgets.QWidget):
    CELL_NUM = 25
    
    def __init__ (self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 1000)
        self.layout = QtWidgets.QGridLayout(self)
        self.cells = []
        for i in range(self.CELL_NUM * self.CELL_NUM):
            x = int(i / self.CELL_NUM)
            y = i % self.CELL_NUM
            self.cells.append(Cell())
            self.layout.addWidget(self.cells[i], x, y)




class Window(QtWidgets.QWidget):
    HEIGHT = 720
    WIDTH = 1280

    def __init__ (self):
        super().__init__()
        self.setWindowTitle("MINESWEEPER BOT")
        self.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.setFixedSize(QSize(self.WIDTH, self.HEIGHT))
        self.layout = QtWidgets.QHBoxLayout(self)
    
        self.field = Field()
        self.start_button = QtWidgets.QPushButton("START")
        self.start_button.clicked.connect(self.foo)

        self.layout.addWidget(self.field)
        self.layout.addWidget(self.start_button)


    @Slot()
    def foo(self):
        print("function doing something")



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window() 
    window.show()

    sys.exit(app.exec())