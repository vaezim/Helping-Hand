from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtWidgets import QProgressBar, QLabel, QPushButton


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # window size
        self.width = 800
        self.height = 800

        # main window setup (size etc.)
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Online cheater Bot for chess.com")
        self.setEnabled(True)
        self.resize(800, 826)
        self.setMinimumSize(QtCore.QSize(self.width, self.height+26))
        self.setMaximumSize(QtCore.QSize(self.width, self.height+26))
        self.setToolTip("")
        self.setToolTipDuration(0)
        self.setAutoFillBackground(False)
        self.setAcceptDrops(True)
        centralwidget = QtWidgets.QWidget()
        centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(centralwidget)

        # set the position of main window on the screen
        self.MainWindowScreenPosition()

        # main frame
        self.frame = QtWidgets.QFrame(centralwidget)
        self.frame.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QPoint(self.width, self.height)))
        self.frame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # frame components
        self.EvalBar()
        self.EvalLabel()
        self.BoardSVG()
        self.BestMoveButton()

    def BestMoveButton(self):
        self.button = QPushButton('Show Best Move!', self.frame)
        self.button.setGeometry(QtCore.QRect(QtCore.QPoint(round(0.2*self.width)+480,round(0.05*self.height)+40), 
                                QtCore.QPoint(round(0.2*self.width)+600,round(0.05*self.height)+90)))
        Font = QtGui.QFont("Helvetica", 10)
        Font.setBold(True)
        self.button.setFont(Font)
        
    def BoardSVG(self, filename="empty_board.svg", replace=False):
        if replace:
            self.board.close()
        self.board = QtSvg.QSvgWidget(filename, self.frame)
        self.board.setGeometry(
            QtCore.QRect(QtCore.QPoint(round(0.2*self.width), round(0.05*self.height)+100), 
                         QtCore.QPoint(round(0.2*self.width)+600, round(0.05*self.height)+700)))
        self.board.show()

    def EvalBar(self):
        # create a vertical progress bar
        self.bar = QProgressBar(self.frame)
        self.bar.setGeometry(
            QtCore.QRect(QtCore.QPoint(round(0.05*self.width), round(0.05*self.height)), 
                         QtCore.QPoint(round(0.05*self.width+50), round(0.95*self.height))))
        self.bar.setValue(50)
        self.bar.setOrientation(QtCore.Qt.Vertical)
        self.bar.setTextVisible(False)

        # black & white chess style eval bar
        CHESS_STYLE = """
            QProgressBar {
                border: 2px solid grey;
                text-align: center;
                background-color: #404040;
            }
            QProgressBar::chunk {
                background-color: white;
            } """
        self.bar.setStyleSheet(CHESS_STYLE)

    def EvalLabel(self):
        self.label = QLabel("0.0", self.frame)
        self.label.move(round(0.05*self.width)+60, round(0.05*self.height))
        self.label.setGeometry(
                QtCore.QRect(QtCore.QPoint(round(0.05*self.width)+60, round(0.05*self.height)), 
                             QtCore.QPoint(round(0.05*self.width)+200, round(0.05*self.height)+50)))
        # set Font
        Font = QtGui.QFont("Helvetica", 25)
        Font.setBold(True)
        self.label.setFont(Font)

    def changeEval(self, eval_num):
        # change the label text
        self.label.setText(str(eval_num))
        # change the bar
        self.bar.setValue(round(50+(eval_num/8*50)))

    def MainWindowScreenPosition(self):
        screen = QDesktopWidget().screenGeometry()
        W, H = screen.width(), screen.height()
        self.move(W-round(1.05*self.width), round(0.05*self.height))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
    