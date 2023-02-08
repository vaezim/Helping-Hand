from PyQt5.QtCore import QThread, pyqtSignal


class UpdateThread(QThread):
    evalSignal = pyqtSignal(float)
    boardSignal = pyqtSignal(str)

    def udpateEval(self, new_eval):
        self.evalSignal.emit(new_eval)

    def updateBoard(self, new_board):
        self.boardSignal.emit(new_board)
        