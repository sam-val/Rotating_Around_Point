from PyQt5.Qt import *
import sys
from collections import deque

# Colours:
EMPTY = 'gray'
CENTER = 'red'
BODY = 'midnightblue'

class Cube(QWidget):
    clicked = pyqtSignal()
    right_clicked = pyqtSignal()
    def __init__(self, width, x, y):
        super().__init__()
        self.width = width
        self.setFixedSize(self.width, self.width)
        self.setAutoFillBackground(True)
        self.colour = EMPTY
        self.pos = x, y
        self.states = deque([0,1,2])
        self.changeColour(self.colour)

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        if e.button() == Qt.RightButton:
            self.right_clicked.emit()

    def changeColour(self, colour):
        pallete = self.palette()
        pallete.setColor(QPalette.Window, QColor(colour))
        self.setPalette(pallete)

class MyWin(QMainWindow):
    def __init__(self,  width, height, cube_width=30):
        super().__init__()
        self.cube_w = cube_width
        self.width = width
        self.height = height
        # Layout -- making the grid
        self.grid = QGridLayout()
        self.grid.setSpacing(2)
        self.make_grid(self.width,self.height)
        self.center_cube = None
        self.body = set()
        self.rot_direction = False # true is clockwise, false is counter clockwise

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
                cube.right_clicked.connect(self.rotateShape)

    def rotateShape(self):
        if self.center_cube:
            # make rotation matrix:
            trans_matrix = [[0, -1],
                            [1,  0]] if self.rot_direction else [[0 , 1],
                                                                 [-1, 0]]
            new_body = []

            # make a new shape (list that contains cube pos)
            for x,y in self.body:
                center_x, center_y = self.center_cube.pos
                # find relative vector (pointing from center cube to the current cube
                rel_x, rel_y = center_x - x, center_y - y
                # compute new relative vector:
                new_rel_x = rel_x * trans_matrix[0][0] + rel_y * trans_matrix[0][1]
                new_rel_y = rel_x * trans_matrix[1][0] + rel_y * trans_matrix[1][1]
                # compute relative back to normal vector(that means it starts from 0,0)
                # which is the sum of relative vec and vector of the center:
                new_pos = new_rel_x + center_x, new_rel_y + center_y
                new_body.append(new_pos)

            self.body = set(new_body)

            # then redraw it on screen:
            for y in range(self.height):
                for x in range(self.width):
                    cube = self.grid.itemAtPosition(x, y).widget()
                    if cube == self.center_cube:
                        pass
                    elif (x,y) not in self.body:
                        self.changeState(cube, at=0)
                        cube.changeColour(EMPTY)
                    else:
                        self.changeState(cube, at=1)
                        cube.changeColour(BODY)

        else:
            print("No center cube selected")


    def changeRotationDirection(self):
        self.rot_direction = not self.rot_direction
        print("Rotation:","Clockwise" if self.rot_direction else "Counter Clockwise" )

    def cube_is_clicked(self):
        cube = self.sender()
        pos = cube.pos
        # print("state: ", cube.states[0])

        # change to next state: 0 -> 1; 1 -> 2; 2 -> 3;
        self.changeState(cube)
        next_state = cube.states[0]

        if next_state == 0:
            if pos in self.body:
                self.body.remove(pos)
            elif cube == self.center_cube:
                self.center_cube = None
            cube.changeColour(EMPTY)

        elif next_state == 1:
            if pos not in self.body:
                self.body.add(pos)
            cube.changeColour(BODY)

        elif next_state == 2:
            if self.center_cube != None:
                # is there is already a center cube, grab it:
                current_cen_x, current_cen_y = self.center_cube.pos
                cen_cube = self.grid.itemAtPosition(current_cen_x, current_cen_y).widget()

                # change state of current center cube to 0 and chnage it's colour:
                self.changeState(cen_cube, at=0)
                cen_cube.changeColour(EMPTY)

                # and set the current cube to the center, and it's colour:
                self.center_cube = cube
                cube.changeColour(CENTER)
            else:
                self.center_cube = cube
                cube.changeColour(CENTER)

            # now it is the center cube, remove it from the body:
            if pos in self.body:
                self.body.remove(pos)

    def changeState(self, cube, at=None):
        if at is None:
            cube.states.rotate(-1)
        else:
            while True:
                cube.states.rotate(-1)
                cur = cube.states[0]
                if cur == at:
                    break

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Q:
            self.close_win()
        elif key == Qt.Key_R:
            self.changeRotationDirection()

    def close_win(self):
        print('closing app...')
        self.close()

WIDTH, HEIGHT = 6, 6
CUBE_WIDTH = 120
app = QApplication(sys.argv)
win = MyWin(WIDTH,HEIGHT,CUBE_WIDTH)

## align cetner
new_rect = QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, win.size(),
                              app.desktop().availableGeometry())
win.setGeometry(new_rect)

sys.exit(app.exec_())

