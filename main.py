import sys
from PyQt5.QtWidgets import qApp, QAction, QMainWindow, QApplication, QWidget, QToolTip, QPushButton, QToolBar, QSplitter, QHBoxLayout, QOpenGLWidget
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QDialog, QGridLayout, QGroupBox, QLabel, QFontDialog, QMessageBox, QStyleFactory, QFrame
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, pyqtSlot, Qt, QBasicTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import PyQt5.QtOpenGL
import demezkeyvalue #:D Thanks, Demez!

class ThwackerMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.Setup()

    def ReadVmf(self,vmf):
        keyvalueRootObject = demezkeyvalue.ReadFile('./test.vmf')
        worldValues = keyvalueRootObject.GetItem('world')
        if worldValues:
            solidList = worldValues.GetAllItems("solid")
            if solidList:
                for solid in solidList:
                    sideList = solid.GetAllItems("side")
                    for side in sideList:
                        sidePlane = side.GetItemValue('plane')
                        vert = []
                        for vertVal in sidePlane.split():
                            print(vertVal)
                            vert.append(0.01*int(vertVal.replace('(','').replace(')','')))
                            if len(vert) == 3:
                                self.VMFVerts.append(vert)
                                vert = []

        print(self.VMFVerts)
        
    def Setup(self):
        self.setWindowTitle("Thwacker")
        self.setWindowIcon(QIcon())

        self.setMinimumSize(QSize(750,500))

        #ContentSections
        self.Content = QGroupBox()
        self.ContentLayout = QGridLayout()

        # ToolBar
        ToolsToolBar = QToolBar('Tools')
        self.Tools = self.addToolBar(Qt.LeftToolBarArea,ToolsToolBar)

        #OpenGl
        self.GlViewport = QOpenGLWidget()
        self.GlViewport.initializeGL()
        self.GlViewport.paintGL = self.paintGL
        self.GlViewport.initializeGL = self.initializeGL

        self._glTimer = QBasicTimer()
        self._glTimer.start(1000/60, self)

        self.VMFVerts = []
        self.ReadVmf('./test.vmf')
        
        self.ContentLayout.addWidget(self.GlViewport,0,0)
        gluPerspective(45, self.width()/self.height(), 0.1, 50)

        self.Triangle = self.VMFVerts
        self.Indices = [] ;
        for i in range(len(self.VMFVerts)): self.Indices.append(i)
        

        self.Content.setLayout(self.ContentLayout)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setCentralWidget(self.Content)
        self.showMaximized()
        self.update()

    def resizeEvent(self,event):
        gluPerspective(45, self.width()/self.height(), 0.1, 50)

    def initializeGL(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)


    def paintGL(self):
        gluPerspective(45, self.width()/self.height(), 0.1, 50)
        glViewport(0, 0, self.GlViewport.width(), self.GlViewport.height())
        gluLookAt(12, 12, 12, 0, 0, 0, 0, 1, 0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClear(GL_COLOR_BUFFER_BIT)

        glRotatef(90,1,0,0)

        glBegin(GL_TRIANGLES)

        for i in self.Indices:
            glVertex3fv(self.Triangle[i])

        glEnd()
        glFinish()
    
    def timerEvent(self, QTimerEvent):
        self.GlViewport.update()

def main():
    app = QApplication(sys.argv)
    Program = ThwackerMainWindow()
    sys.exit(app.exec_())

main()
