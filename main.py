import sys
from random import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette, QPainter, QPen, QBrush, QColor
from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QStyleOption

class Cell:
    def __init__(self, x, y, mine):
        self.x = x
        self.y = y
        self.mine = mine





class Field(QtWidgets.QWidget):
    
    CELL_NUM = 25
    CELL_SIZE = 10
    
    def __init__ (self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 1000)
        self.layout = QtWidgets.QGridLayout(self)
        self.cells = []
        for i in range(self.CELL_NUM * self.CELL_NUM):
            x = int(i / self.CELL_NUM)
            y = i % self.CELL_NUM
            isMine = random() > 0.9
            self.cells.append(Cell(x, y, isMine))

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - self.CELL_SIZE * rect.height() / self.CELL_SIZE
        for cell in self.cells:
            color = QColor.fromRgb(255, 0, 0) if cell.mine else QColor.fromRgb(0, 255, 0)
            self.draw_square(painter, rect.left() + cell.x * self.CELL_SIZE, boardtop + cell.y * self.CELL_SIZE, color)
        

    def draw_square(self, painter, x, y, color):
        rect = self.contentsRect()
        painter.fillRect(x + 1, y + 1, rect.width() / self.CELL_SIZE - 2, rect.height() / self.CELL_SIZE - 2, color)


        


    
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