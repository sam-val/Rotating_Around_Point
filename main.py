from PyQt5.Qt import *
import sys

class Cube(QWidget):
    clicked = pyqtSignal()
    def __init__(self, width):
        super().__init__()
        self.width = width
        self.setFixedSize(self.width, self.width)
        self.setAutoFillBackground(True)
        self.colour = 'blue'

        self.changeColour(self.colour)

    def mousePressEvent(self, e) -> None:
        self.clicked.emit()
        self.changeColour('red')

    def changeColour(self, colour):
        pallete = self.palette()
        pallete.setColor(QPalette.Window, QColor(colour))
        self.setPalette(pallete)




class MyWin(QMainWindow):
    def __init__(self, cube_width=30):
        super().__init__()
        self.cube_w = cube_width
        # Layout -- making the grid
        self.grid = QGridLayout()
        self.grid.setSpacing(2)
        self.make_grid(4,4)

        # Create a dummy widget
        dummy_widget = QWidget()
        dummy_widget.setLayout(self.grid)

        ## and set it...
        self.setCentralWidget(dummy_widget)
        self.show()

    def make_grid(self, w, h):
        for y in range(h):
            for x in range(w):
                cube = Cube(self.cube_w)
                self.grid.addWidget(cube, x, y, 1, 1)
                # cube.clicked.connect(self.cube_is_clicked)

    # def cube_is_clicked(self):
    #     print("hello")

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Q:
            self.close_win()

    def close_win(self):
        print('closing app...')
        self.close()

CUBE_WIDTH = 100
app = QApplication(sys.argv)
win = MyWin(CUBE_WIDTH)

sys.exit(app.exec_())

