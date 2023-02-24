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
        self.mines_around = 0
    

class Field(QtWidgets.QWidget):
    
    CELL_NUM = 20
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
            isMine = random() > 0.9
            self.cells.append(Cell(int(i / self.CELL_NUM), i % self.CELL_NUM, isMine))
        for cell in self.cells:
            cell.mines_around = self.mines_around(cell)

    def paintEvent(self, event):
        rect = self.contentsRect()
        painter = QPainter(self)
        painter.fillRect(0, 0, self.FIELD_SIZE, self.FIELD_SIZE, QColor(0, 0, 0))
        for cell in self.cells:
            self.draw_cell(painter, cell)
        
    #TODO: better code
    def draw_cell(self, painter, cell):
        x = cell.j * (self.CELL_SIZE + self.CELL_OFFSET) + self.CELL_OFFSET
        y = cell.i * (self.CELL_SIZE + self.CELL_OFFSET) + self.CELL_OFFSET
        if cell.opened & cell.mine:
            color = QColor.fromRgb(255, 0, 0)
        elif cell.opened:
                color = QColor.fromRgb(0, 255, 0)
        else:
            color = QColor.fromRgb(99, 92, 92)
        painter.fillRect(x, y, self.CELL_SIZE, self.CELL_SIZE, color)
        if (cell.opened) & (cell.mine == False):
            font = painter.font()
            font.setPixelSize(self.CELL_SIZE)
            painter.setFont(font)
            painter.setPen(QColor.fromRgb(0, 0, 0))
            painter.drawText(x + self.CELL_SIZE * 1/10, y + self.CELL_SIZE * 3/4, str(cell.mines_around))

    def mines_around(self, cell):
        i = cell.i
        j = cell.j
        id = i * self.CELL_NUM + j
        num = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                neighbour_id = (i + di) * self.CELL_NUM + j + dj 
                if (neighbour_id >= 0) & (neighbour_id < len(self.cells)):
                    num += 1 if self.cells[neighbour_id].mine == True else 0
        return num

    def mousePressEvent(self, event):
        i = int((event.y() - self.CELL_OFFSET) / (self.CELL_SIZE + self.CELL_OFFSET))
        j = int((event.x() - self.CELL_OFFSET) / (self.CELL_SIZE + self.CELL_OFFSET))
        id = int(i * self.CELL_NUM + j)
        self.cells[id].opened = True
        print(self.cells[id].mines_around)
        self.repaint()

    #TODO
    def open_neighbour(self, cell):
        cell.opened = True
        if cell.mines_around == 0:
            i = cell.i
            j = cell.j
            if self.get_cell(i - 1, j):
                self.open_neighbour(self.cells[cell.j - 1])
    #TODO
    def get_cell(self, i, j):
        return self.cells[j * self.CELL_NUM + i]

    def open_all(self):
        for cell in self.cells:
            cell.opened = True
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
        self.field.open_all()
        print("function doing something")



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window() 
    window.show()
    sys.exit(app.exec())