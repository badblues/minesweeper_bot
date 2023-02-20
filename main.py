import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class Cell(QtWidgets.QWidget):
    SIZE = 20

    def __init__ (self, i, j):
        super().__init__()
        
        self.i = i
        self.j = j

        

        

 


class Field(QtWidgets.QWidget):
    CELL_NUM = 50
    
    def __init__ (self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 1000)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.cells = []
        for i in range(self.CELL_NUM * self.CELL_NUM):
            self.cells.append(Cell(int(i / self.CELL_NUM), i % self.CELL_NUM))
            self.layout.addWidget(self.cells[i])




class Window(QtWidgets.QWidget):
    HEIGHT = 720
    WIDTH = 1280

    def __init__ (self):
        super().__init__()
        self.setGeometry(0, 0, self.WIDTH, self.HEIGHT)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.field = Field()

        self.start_button = QtWidgets.QPushButton("START")
        self.start_button.clicked.connect(self.foo)

        self.layout.addWidget(self.field)
        self.layout.addWidget(self.start_button)


    @QtCore.Slot()
    def foo(self):
        print("function doing something")



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window() 
    window.show()

    sys.exit(app.exec())