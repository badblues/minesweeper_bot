import time
import sys
from random import random
from PySide6 import QtWidgets, QtUiTools
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import QStyleOption
from PySide6.QtUiTools import QUiLoader

#TODO: better mines spawning alg
#TODO: check code style
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
    
    CELL_NUM = 30
    FIELD_SIZE = 700
    CELL_OFFSET = 1
    CELL_SIZE = (FIELD_SIZE - (CELL_NUM + 1) * CELL_OFFSET) / CELL_NUM
    MINE_CHANCE = 0.1
    
    game_stopped = False
    
    def __init__ (self, window):
        super().__init__()
        print(self.FIELD_SIZE, self.CELL_NUM, self.CELL_SIZE, self.CELL_OFFSET)
        self.window = window
        self.setMinimumSize(self.FIELD_SIZE, self.FIELD_SIZE)
        self.setMaximumSize(self.FIELD_SIZE, self.FIELD_SIZE)
        self.cells = []
        self.generate()


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
            color = QColor.fromRgb(26, 189, 14)
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
        if event.button() == Qt.MouseButton.LeftButton:
            self.open_cell(i, j)
        elif event.button() == Qt.MouseButton.RightButton:
            self.flag_cell(i, j)
            


    def open_cell(self, i, j):
        if self.game_stopped:
            return
        cell = self.get_cell(i, j)
        if not cell.flag:
            if (cell.mine):
                cell.opened = True
                self.stop_game()
            else:
                self.open_neighbour(cell)
                if self.check_for_win():
                    self.stop_game() 
        self.repaint()


    def flag_cell(self, i, j):
        if self.game_stopped:
            return
        cell = self.get_cell(i, j)
        if not cell.opened:
            cell.flag = not cell.flag
        self.repaint()


    def stop_game(self):
        self.game_stopped = True
        for cell in self.cells:
            if cell.mine:
                cell.flag = False
                cell.opened = True


    def check_for_win(self):
        for cell in self.cells:
            if (not cell.mine) & (not cell.opened):
                return False
        return True


    def open_neighbour(self, cell):
        if (cell.mines_around == 0) & (not cell.opened):
            cell.opened = True
            #self.repaint()
            i = cell.i
            j = cell.j
            if self.get_cell(i - 1, j):
                self.open_neighbour(self.cells[(i - 1) * self.CELL_NUM + j])
            if self.get_cell(i - 1, j - 1):
                self.open_neighbour(self.cells[(i - 1) * self.CELL_NUM + j - 1])
            if (self.get_cell(i, j - 1)):
                self.open_neighbour(self.cells[i * self.CELL_NUM + j - 1])
            if self.get_cell(i + 1, j - 1):
                self.open_neighbour(self.cells[(i + 1) * self.CELL_NUM + j - 1])
            if (self.get_cell(i + 1, j)):
                self.open_neighbour(self.cells[(i + 1) * self.CELL_NUM + j])
            if self.get_cell(i + 1, j + 1):
                self.open_neighbour(self.cells[(i + 1) * self.CELL_NUM + j + 1])
            if (self.get_cell(i, j + 1)):
                self.open_neighbour(self.cells[i * self.CELL_NUM + j + 1])
            if self.get_cell(i - 1, j + 1):
                self.open_neighbour(self.cells[(i - 1) * self.CELL_NUM + j + 1])
        elif not cell.mine:
            cell.opened = True


    def get_cell(self, i, j):
        if (i >= 0) & (i < self.CELL_NUM) & (j >= 0) & (j < self.CELL_NUM):
            return self.cells[i * self.CELL_NUM + j]
        return None


    def generate(self):
        self.game_stopped = False
        self.cells.clear()
        for i in range(self.CELL_NUM * self.CELL_NUM):
            isMine = random() > (1 - self.MINE_CHANCE)
            self.cells.append(Cell(int(i / self.CELL_NUM), i % self.CELL_NUM, isMine))
        for cell in self.cells:
            cell.mines_around = self.mines_around(cell)
        self.repaint()
        

class Solver:

    def __init__(self, field):
        self.field = field
        self.cell_num = field.CELL_NUM
        print(self.cell_num)


    def gameloop(self):
        if not self.field.game_stopped:
            i = int(random() * self.cell_num)
            j = int(random() * self.cell_num)
            self.field.open_cell(i, j)
            time.sleep(0.2)
            self.gameloop()            


    def solve(self):
        self.gameloop()

    
class Window(QtWidgets.QMainWindow):

    WIDTH = 1280
    HEIGHT = 720

    def __init__ (self):
        super().__init__()
        self.setWindowTitle("MINESWEEPER BOT")
        self.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.setFixedSize(QSize(self.WIDTH, self.HEIGHT))
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.h_layout = QtWidgets.QHBoxLayout(self.centralWidget())
        self.field_layout = QtWidgets.QHBoxLayout(self.centralWidget())
        self.field_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout = QtWidgets.QVBoxLayout(self.centralWidget())
        self.menu_layout.setSpacing(30)
        self.h_layout.addLayout(self.field_layout, 3)
        self.h_layout.addLayout(self.menu_layout, 1)
        print(self.h_layout.stretch(0), self.h_layout.stretch(1))
        self.centralWidget().show()
        self.field = Field(self)
        self.restart_button = QtWidgets.QPushButton("RESTART")
        self.restart_button.clicked.connect(self.restart)
        self.solve_button = QtWidgets.QPushButton("SOLVE")
        self.solve_button.clicked.connect(self.solve)
        font = QFont()
        font.setFamily("Ramabhadra")
        font.setPointSize(36)
        self.label = QtWidgets.QLabel("MINESWEEPER")
        self.label.setFont(font)
        self.label.setMaximumSize(320, 50)
        self.label.setAlignment(Qt.AlignCenter)
        menu_spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        field_spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.field_layout.addItem(field_spacer)
        self.field_layout.addWidget(self.field)
        self.field_layout.addItem(field_spacer)
        self.menu_layout.addWidget(self.label, 2)
        self.menu_layout.addWidget(self.restart_button, 1)
        self.menu_layout.addWidget(self.solve_button, 1)
        self.menu_layout.addItem(menu_spacer)
        self.solver = Solver(self.field)


    @Slot()
    def restart(self):
        self.field.generate()


    @Slot()
    def solve(self):
        self.solver.solve()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window() 
    window.show()
    sys.exit(app.exec())