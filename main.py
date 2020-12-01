from PyQt5.Qt import *
import sys
from collections import deque

class Cube(QWidget):
    clicked = pyqtSignal()
    def __init__(self, width, x, y):
        super().__init__()
        self.width = width
        self.setFixedSize(self.width, self.width)
        self.setAutoFillBackground(True)
        self.colour = 'gray'
        self.pos = x, y
        self.states = deque([0,1,2])

        self.changeColour(self.colour)

    def mousePressEvent(self, e) -> None:
        # print(self.x, self.y)
        self.clicked.emit()
        # self.changeColour('red')

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
        self.center_cube = None
        self.body = set()

        # Create a dummy widget
        dummy_widget = QWidget()
        dummy_widget.setLayout(self.grid)

        ## and set it...
        self.setCentralWidget(dummy_widget)
        self.show()

    def make_grid(self, w, h):
        for y in range(h):
            for x in range(w):
                cube = Cube(self.cube_w, x, y)
                self.grid.addWidget(cube, x, y, 1, 1)
                cube.clicked.connect(self.cube_is_clicked)

    def cube_is_clicked(self):
        cube = self.sender()
        pos = cube.pos

        # change to next state: 0 -> 1; 1 -> 2; 2 -> 3;
        self.changeState(cube)
        next_state = cube.states[0]

        if next_state == 0:
            if pos in self.body:
                self.body.remove(pos)
            elif cube == self.center_cube:
                self.center_cube = None
            cube.changeColour('gray')

        elif next_state == 1:
            if pos not in self.body:
                self.body.add(pos)
            cube.changeColour("red")

        elif next_state == 2:
            if self.center_cube != None:
                # is there is already a center cube, grab it:
                current_cen_x, current_cen_y = self.center_cube.pos
                cen_cube = self.grid.itemAtPosition(current_cen_x, current_cen_y).widget()
                print(type(cen_cube))

                # change state of current center cube to 1, add it to the body and chnage it's colour:
                self.changeState(cen_cube, at=1)
                self.body.add(cen_cube.pos)
                cen_cube.changeColour('red')

                # and set the current cube to the center, and it's colour:
                self.center_cube = cube
                cube.changeColour('green')
            else:
                self.center_cube = cube
                cube.changeColour("green")

            # now it is the center cube, remove it from the body:
            if pos in self.body:
                self.body.remove(pos)

        print('center cube pos is', f'{self.center_cube.pos}' if self.center_cube is not None else 'None')
        print(f'body: {self.body}')

    def setCenterCube(self, cube):
        pass

    def changeState(self, cube, at=None):
        if not at:
            cube.states.rotate(-1)
        else:
            while True:
                cube.states.rotate(1)
                cur = cube.states[0]
                if cur == at:
                    break

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

