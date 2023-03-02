import sys
from random import random
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6.QtCore import *

# Cell might be opened OR flagged no matter it being a mine or not
class Cell:
  def __init__(self, i, j, mine):
    self.i = i
    self.j = j
    self.mine = mine
    self.opened = False
    self.mines_around = 0
    self.flag = False


class Field(QtWidgets.QWidget):

  FIELD_SIZE = 700
  CELL_OFFSET = 1

  def __init__(self, window):
    super().__init__()
    self.window = window
    self.setMinimumSize(self.FIELD_SIZE, self.FIELD_SIZE)
    self.setMaximumSize(self.FIELD_SIZE, self.FIELD_SIZE)
    self.cells = []
    self.mine_chance = 0.15
    self.game_stopped = False
    self.cell_num = 15
    self.cell_size = (self.FIELD_SIZE - (self.cell_num + 1)
                      * self.CELL_OFFSET) / self.cell_num
    self.generate()

  def paintEvent(self):
    painter = QPainter(self)
    painter.fillRect(0, 0, self.FIELD_SIZE, self.FIELD_SIZE, QColor(0, 0, 0))
    for cell in self.cells:
      self.draw_cell(painter, cell)

  def draw_cell(self, painter, cell):
    x = cell.j * (self.cell_size + self.CELL_OFFSET) + self.CELL_OFFSET
    y = cell.i * (self.cell_size + self.CELL_OFFSET) + self.CELL_OFFSET
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
    painter.fillRect(x, y, self.cell_size, self.cell_size, color)
    font = painter.font()
    font.setPixelSize(self.cell_size)
    painter.setFont(font)
    painter.setPen(QColor.fromRgb(0, 0, 0))
    painter.drawText(x + self.cell_size * 1/10, y + self.cell_size * 3/4, sym)

  def mines_around(self, cell):
    i = cell.i
    j = cell.j
    num = 0
    for di in [-1, 0, 1]:
      for dj in [-1, 0, 1]:
        neighbour = self.get_cell(i + di, j + dj)
        if neighbour:
          if neighbour.mine:
            num += 1
    return num

  def mousePressEvent(self, event):
    i = int((event.position().y() - self.CELL_OFFSET) /
            (self.cell_size + self.CELL_OFFSET))
    j = int((event.position().x() - self.CELL_OFFSET) /
            (self.cell_size + self.CELL_OFFSET))
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
        self.window.gameover(False)
      else:
        self.open_neighbour(cell)
        if self.check_for_win():
          self.stop_game()
          self.window.gameover(True)
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
      i = cell.i
      j = cell.j
      for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
          cell = self.get_cell(i + di, j + dj)
          if cell:
            self.open_neighbour(cell)
    elif not cell.mine:
      cell.opened = True

  def get_cell(self, i, j):
    if (i >= 0) & (i < self.cell_num) & (j >= 0) & (j < self.cell_num):
      return self.cells[i * self.cell_num + j]
    return None

  def generate(self):
    self.game_stopped = False
    self.cells.clear()
    for i in range(self.cell_num * self.cell_num):
      isMine = random() > (1 - self.mine_chance)
      self.cells.append(Cell(int(i / self.cell_num), i %
                             self.cell_num, isMine))
    for cell in self.cells:
      cell.mines_around = self.mines_around(cell)
    self.repaint()

  def closed_cells(self):
    closed = []
    for cell in self.cells:
      if (not cell.opened) & (not cell.flag):
        closed.append(cell)
    return closed

  def set_mine_chance(self, chance):
    self.mine_chance = chance
    self.generate()

  def set_cells_num(self, num):
    self.cell_num = num
    self.cell_size = (self.FIELD_SIZE - (self.cell_num + 1) *
                      self.CELL_OFFSET) / self.cell_num
    self.generate()

class Solver:

  def __init__(self, field):
    self.field = field
    self.cell_num = field.cell_num

  def gameloop(self):
    while not self.field.game_stopped:
      did_smth = False
      for i in range(self.cell_num):
        for j in range(self.cell_num):
          cell = self.field.get_cell(i, j)
          if cell.opened:
            if cell.mines_around != 0:
              if self.look_around(cell):
                did_smth = True
      if not did_smth:
        self.random_guess()

  def look_around(self, cell):
    n = cell.mines_around
    i = cell.i
    j = cell.j
    if n > 0:
      closed_cells = []
      flagged_cells = []
      for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
          n_cell = self.field.get_cell(i + di, j + dj)
          if n_cell:
            if not n_cell.opened:
              if n_cell.flag:
                flagged_cells.append(n_cell)
              else:
                closed_cells.append(n_cell)
      if len(closed_cells) != 0:
        # all closed cells are safe
        if len(flagged_cells) == n:  
          for c in closed_cells:
            self.field.open_cell(c.i, c.j)
          return True
        # all closed cells are mines
        elif (len(closed_cells) + len(flagged_cells)) == n:  
          for c in closed_cells:
            self.field.flag_cell(c.i, c.j)
          return True
      return False
    return False

  def random_guess(self):
    closed = self.field.closed_cells()
    i = int(random() * len(closed))
    self.field.open_cell(closed[i].i, closed[i].j)

  def solve(self):
    self.cell_num = self.field.cell_num
    self.gameloop()


class Window(QtWidgets.QMainWindow):

  WIDTH = 1280
  HEIGHT = 720

  def __init__(self):
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
    self.centralWidget().show()
    self.field = Field(self)
    self.restart_button = QtWidgets.QPushButton("RESTART")
    self.restart_button.clicked.connect(self.restart)
    self.solve_button = QtWidgets.QPushButton("SOLVE")
    self.solve_button.clicked.connect(self.solve)
    self.slider = QtWidgets.QSlider(Qt.Horizontal)
    self.slider.setMaximum(50)
    self.slider.setSingleStep(1)
    self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
    self.slider.setTickInterval(5)
    self.slider.setCursor(Qt.ClosedHandCursor)
    self.slider.setValue(self.field.mine_chance * 100)
    self.slider.valueChanged.connect(self.slider_change)
    self.input_line = QtWidgets.QLineEdit()
    self.input_line.setMaximumSize(50, 40)
    self.input_line.setMaxLength(2)
    self.input_line.setAlignment(Qt.AlignCenter)
    self.input_line.setValidator(QIntValidator())
    self.input_line.textChanged.connect(self.input_line_change)
    font = QFont()
    font.setFamily("Ramabhadra")
    font.setPointSize(36)
    self.label = QtWidgets.QLabel("MINESWEEPER")
    self.label.setFont(font)
    self.label.setMaximumSize(320, 50)
    self.label.setAlignment(Qt.AlignCenter)
    menu_spacer = QtWidgets.QSpacerItem(
        10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    field_spacer = QtWidgets.QSpacerItem(
        10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
    self.field_layout.addItem(field_spacer)
    self.field_layout.addWidget(self.field)
    self.field_layout.addItem(field_spacer)
    self.menu_layout.addWidget(self.label, 2)
    self.menu_layout.addWidget(self.restart_button, 1)
    self.menu_layout.addWidget(self.solve_button, 1)
    self.menu_layout.addWidget(self.slider, 1)
    h_lay = QtWidgets.QHBoxLayout()
    h_lay.addWidget(self.input_line)
    self.menu_layout.addLayout(h_lay, 1)
    self.menu_layout.addItem(menu_spacer)
    self.solver = Solver(self.field)

  @Slot()
  def restart(self):
    self.label.setText("MINESWEEPER")
    self.field.generate()

  @Slot()
  def solve(self):
    if (not self.field.game_stopped):
      self.label.setText("SOLVING...")
      self.solver.solve()

  @Slot()
  def slider_change(self):
    self.field.set_mine_chance(self.slider.value() / 100)

  @Slot()
  def input_line_change(self):
    if self.input_line.text() != "":
      if self.input_line.text()[0] != "-":
        num = int(self.input_line.text())
        if (num > 0) & (num <= 40):
          self.field.set_cells_num(num)

  def gameover(self, win):
    if win:
      self.label.setText("!!WIN!!")
    else:
      self.label.setText("!!BOMBED!!")


if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  window = Window()
  window.show()
  sys.exit(app.exec())
