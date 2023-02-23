import sys
from random import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette, QPainter, QPen, QBrush, QColor
from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QStyleOption

class Cell:
    def __init__(self, i, j, mine):
        self.i = i
        self.j = j
        self.mine = mine
        self.opened = False
    

class Field(QtWidgets.QWidget):
    
    CELL_NUM = 33
    FIELD_SIZE = 551
    CELL_OFFSET = 1
    CELL_SIZE = (FIELD_SIZE - (CELL_NUM + 1) * CELL_OFFSET) / CELL_NUM
    
    def __init__ (self):
        super().__init__()
        print(self.FIELD_SIZE, self.CELL_NUM, self.CELL_SIZE, self.CELL_OFFSET)
        self.setGeometry(100, 100, self.FIELD_SIZE, self.FIELD_SIZE)
        self.layout = QtWidgets.QGridLayout(self)
        self.cells = []
        self.contentsRect().setWidth(self.FIELD_SIZE)
        self.contentsRect().setHeight(self.FIELD_SIZE)
        for i in range(self.CELL_NUM * self.CELL_NUM):
            x = i % self.CELL_NUM
            y = int(i / self.CELL_NUM)
            isMine = random() > 0.9
            self.cells.append(Cell(x, y, isMine))
        self.cells[0].opened = True
        self.cells[5].opened = True
        self.cells[10].opened = True
        self.cells[15].opened = True
        self.cells[20].opened = True

    def paintEvent(self, event):
        rect = self.contentsRect()
        painter = QPainter(self)
        painter.fillRect(0, 0, self.FIELD_SIZE, self.FIELD_SIZE, QColor(0, 0, 0))
        for cell in self.cells:
            self.draw_cell(painter, cell)
        
    def draw_cell(self, painter, cell):
        if cell.opened:
            if cell.mine:
                color = QColor.fromRgb(255, 0, 0)
            else:
                color = QColor.fromRgb(0, 255, 0)
        else:
            color = QColor.fromRgb(99, 92, 92)
        x = cell.i * (self.CELL_SIZE + self.CELL_OFFSET) + self.CELL_OFFSET
        y = cell.j * (self.CELL_SIZE + self.CELL_OFFSET) + self.CELL_OFFSET
        painter.fillRect(x, y, self.CELL_SIZE, self.CELL_SIZE, color)

    def cells_around(self, cell):
        num = 0

    def mousePressEvent(self, event):
        pos_i = int((event.x() - self.CELL_OFFSET) / (self.CELL_SIZE + self.CELL_OFFSET))
        pos_j = int((event.y() - self.CELL_OFFSET) / (self.CELL_SIZE + self.CELL_OFFSET))
        i = int(pos_j * self.CELL_NUM + pos_i)
        print(pos_i, pos_j, i)
        self.cells[i].opened = True
        self.repaint()
        



    
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