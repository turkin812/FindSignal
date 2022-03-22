from PyQt5.QtWidgets import QApplication, QMainWindow
from Plot import Plotling
from Task2_2 import Ui_MainWindow
import sys
from PyQt5 import uic


Form, Window = uic.loadUiType("main.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.btnplot.clicked.connect(self.plot_graph)

	def plot_graph(self):
		f1 = float(self.f1.toPlainText())
		f2 = float(self.f2.toPlainText())
		f3 = float(self.f3.toPlainText())
		fd = float(self.fd.toPlainText())
		N = int(self.NN.toPlainText())
		n0 = int(self.n0.toPlainText())
		n1 = int(self.n1.toPlainText())
		tt = float(self.tt.toPlainText())
		TT = float(self.TT.toPlainText())
		md = Plotling()
		list_t, list_x, list_deviation_t, list_deviation_x = md.t_y_ps(f1, f2, f3, fd, N, n0, n1)
		list_threshold_value, average_error_x, average_error_y, out_del_n0, out_del_n1 = md.filter(N, tt, TT, fd, list_deviation_x, n0, n1)
		md._plot(list_threshold_value, list_t, list_deviation_t, list_x, list_deviation_x, average_error_x, average_error_y)
		self.n0_2.setText(str(out_del_n0))
		self.n1_2.setText(str(out_del_n1))


if __name__ == '__main__':
	#app = QApplication(sys.argv)
	#w = Window()
	#form = Form()
	#form.setupUi(w)
	#w.setWindowTitle('Сигнальщик')
	#w.show()
	#sys.exit(app.exec_())

	app = QApplication(sys.argv)
	w = MainWindow()
	w.setWindowTitle('Шифровальчик')
	w.resize(800, 300)
	w.show()
	sys.exit(app.exec_())