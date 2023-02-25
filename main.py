import sys
from random import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPalette, QPainter, QPen, QBrush, QColor, QMouseEvent
from PySide6.QtCore import QSize, Slot, Qt
from PySide6.QtWidgets import QStyleOption

#TODO: rmb places flag
#TODO: opening mine ends game
#TODO: bot himself

class Cell:
    def __init__(self, i, j, mine):
        self.i = i
        self.j = j
        self.mine = mine
        self.opened = False
        self.mines_around = 0
        self.flag = False
    

class Field(QtWidgets.QWidget):
    
    CELL_NUM = 20
    FIELD_SIZE = 551
    CELL_OFFSET = 1
    CELL_SIZE = (FIELD_SIZE - (CELL_NUM + 1) * CELL_OFFSET) / CELL_NUM
    MINE_CHANCE = 0.1
    
    def __init__ (self):
        super().__init__()
        print(self.FIELD_SIZE, self.CELL_NUM, self.CELL_SIZE, self.CELL_OFFSET)
        self.setGeometry(100, 100, self.FIELD_SIZE, self.FIELD_SIZE)
        self.layout = QtWidgets.QGridLayout(self)
        self.cells = []
        self.contentsRect().setWidth(self.FIELD_SIZE)
        self.contentsRect().setHeight(self.FIELD_SIZE)
        for i in range(self.CELL_NUM * self.CELL_NUM):
            isMine = random() > (1 - self.MINE_CHANCE)
            self.cells.append(Cell(int(i / self.CELL_NUM), i % self.CELL_NUM, isMine))
        for cell in self.cells:
            cell.mines_around = self.mines_around(cell)


    def paintEvent(self, event):
        rect = self.contentsRect()
        painter = QPainter(self)
        painter.fillRect(0, 0, self.FIELD_SIZE, self.FIELD_SIZE, QColor(0, 0, 0))
        for cell in self.cells:
            self.draw_cell(painter, cell)
        

    def draw_cell(self, painter, cell):
        x = cell.j * (self.CELL_SIZE + self.CELL_OFFSET) + self.CELL_OFFSET
        y = cell.i * (self.CELL_SIZE + self.CELL_OFFSET) + self.CELL_OFFSET
        sym = ""
        if cell.opened & cell.mine:
            color = QColor.fromRgb(227, 68, 48)
            sym = "#"
        elif (cell.opened) & (cell.mines_around > 0):
            color = QColor.fromRgb(126, 189, 194)
            sym = str(cell.mines_around)
        elif cell.opened:
            color = QColor.fromRgb(35, 31, 32)
        elif cell.flag:
            color = QColor.fromRgb(126, 189, 214)
            sym = " !"
        else:
            color = QColor.fromRgb(239, 230, 221)
        painter.fillRect(x, y, self.CELL_SIZE, self.CELL_SIZE, color)
        font = painter.font()
        font.setPixelSize(self.CELL_SIZE)
        painter.setFont(font)
        painter.setPen(QColor.fromRgb(0, 0, 0))
        painter.drawText(x + self.CELL_SIZE * 1/10, y + self.CELL_SIZE * 3/4, sym)


    def mines_around(self, cell):
        i = cell.i
        j = cell.j
        num = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                neighbour = self.get_cell(i + di, j + dj)
                if (neighbour):
                    if (neighbour.mine):
                        num += 1
        return num


    def mousePressEvent(self, event):
        i = int((event.position().y() - self.CELL_OFFSET) / (self.CELL_SIZE + self.CELL_OFFSET))
        j = int((event.position().x() - self.CELL_OFFSET) / (self.CELL_SIZE + self.CELL_OFFSET))
        cell = self.get_cell(i, j)
        if (event.button() == Qt.MouseButton.LeftButton) & (not cell.flag):
            self.open_neighbour(cell)
        elif (event.button() == Qt.MouseButton.RightButton) & (not cell.opened):
            cell.flag = not cell.flag
        self.repaint()


    def open_neighbour(self, cell):
        if (cell.mines_around == 0) & (not cell.opened):
            cell.opened = True
            i = cell.i
            j = cell.j
            if self.get_cell(i - 1, j):
                self.open_neighbour(self.cells[(i - 1) * self.CELL_NUM + j])
            if (self.get_cell(i, j - 1)):
                self.open_neighbour(self.cells[i * self.CELL_NUM + j - 1])
            if (self.get_cell(i + 1, j)):
                self.open_neighbour(self.cells[(i + 1) * self.CELL_NUM + j])
            if (self.get_cell(i, j + 1)):
                self.open_neighbour(self.cells[i * self.CELL_NUM + j + 1])
        else:
            cell.opened = True


    def get_cell(self, i, j):
        if (i >= 0) & (i < self.CELL_NUM) & (j >= 0) & (j < self.CELL_NUM):
            return self.cells[i * self.CELL_NUM + j]
        return None

    def open_all(self):
        for cell in self.cells:
            cell.flag = False
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